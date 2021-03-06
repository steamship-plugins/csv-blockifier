"""CSV Blockifier - Steamship Plugin.
"""

import csv
import io
import logging
from typing import Union, List, Optional, Type

from steamship.app import App, create_handler
from steamship.base.error import SteamshipError
from steamship.data.block import Block
from steamship.data.file import File
from steamship.data.tags import Tag
from steamship.plugin.blockifier import Blockifier, Config
from steamship.plugin.inputs.raw_data_plugin_input import RawDataPluginInput
from steamship.plugin.outputs.block_and_tag_plugin_output import BlockAndTagPluginOutput
from steamship.plugin.service import Response, PluginRequest
from pydantic import constr


class CsvBlockifierPlugin(Blockifier, App):
    """"Converts CSV or TSV into Tagged Steamship Blocks."""

    class CsvBlockifierConfig(Config):
        text_column: str
        tag_columns: List[str]
        tag_kind: str = None
        delimiter: Optional[str] = ","
        quotechar: Optional[constr(max_length=1)] = '"'
        escapechar: Optional[constr(max_length=1)] = "\\"
        newline: Optional[str] = "\\n"
        skipinitialspace: Optional[bool] = False

        def __init__(self, **kwargs):
            if isinstance(kwargs.get("tag_columns", None), str):
                kwargs["tag_columns"] = kwargs["tag_columns"].split(",")
            super().__init__(**kwargs)

    def config_cls(self) -> Type[CsvBlockifierConfig]:
        return self.CsvBlockifierConfig

    def _get_text(self, row) -> str:
        text = row.get(self.config.text_column)
        if text:
            text = text.replace(self.config.newline, "\n")
        return text

    def _get_tags(self, row) -> List[str]:
        tag_values = []
        for tag_column in self.config.tag_columns:
            tag_value = row.get(tag_column)
            if tag_value:
                tag_values.append(tag_value.replace(self.config.newline, "\n"))
        return tag_values

    def run(
        self, request: PluginRequest[RawDataPluginInput]
    ) -> Union[Response, Response[BlockAndTagPluginOutput]]:

        if request is None or request.data is None or request.data.data is None:
            raise SteamshipError(message="Missing data field on the incoming request.")

        data = request.data.data
        if isinstance(data, bytes):
            data = data.decode("utf-8")

        if not isinstance(data, str):
            raise SteamshipError(message="The incoming data was not of expected String type")

        reader = csv.DictReader(
            io.StringIO(data),
            delimiter=self.config.delimiter,
            quotechar=self.config.quotechar,
            escapechar=self.config.escapechar,
            skipinitialspace=self.config.skipinitialspace,
        )
        file = File.CreateRequest(blocks=[])
        for row in reader:
            text = self._get_text(row)
            tag_values = self._get_tags(row)

            block = Block.CreateRequest(
                text=text,
                tags=[
                    Tag.CreateRequest(kind=self.config.tag_kind, name=tag_value)
                    for tag_value in tag_values
                ],
            )
            file.blocks.append(block)

        return Response(data=BlockAndTagPluginOutput(file=file))

handler = create_handler(CsvBlockifierPlugin)
