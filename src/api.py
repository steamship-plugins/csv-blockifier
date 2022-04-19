"""CSV Blockifier - Steamship Plugin.
"""

from steamship.app import App, Response, post, create_handler
from steamship.plugin.converter import Converter
from steamship.plugin.service import PluginResponse, PluginRequest
from steamship.base.error import SteamshipError
from steamship.base import MimeTypes
from steamship.data.block import Block
from steamship.data.file import File
from steamship.data.tags import TagKind, DocTag, Tag
from steamship.plugin.inputs.raw_data_plugin_input import RawDataPluginInput
from steamship.plugin.outputs.block_and_tag_plugin_output import BlockAndTagPluginOutput
import csv
import io

class CsvBlockifierPlugin(Converter, App):
    """"Converts CSV or TSV into Tagged Steamship Blocks."""

    def __init__(self, client=None, config=None):
        self.config = config

    def run(self, request: PluginRequest[RawDataPluginInput]) -> PluginResponse[BlockAndTagPluginOutput]:
        if request is None or request.data is None or request.data.data is None:
            return Response(error=SteamshipError(
                message="Missing data field on the incoming request."
            ))

        if type(request.data.data) != str:
            return Response(error=SteamshipError(
                message="The incoming data was not of expected String type"
            ))

        delimiter = self.config.get('delimiter', ',')
        quotechar = self.config.get('quotechar', '"')
        escapechar = self.config.get('escapechar', '\\')
        newline = self.config.get('newline', '\\n')
        skipinitialspace = self.config.get('skipinitialspace', False)

        text_column = self.config.get('text_column', None)
        tag_columns = self.config.get('tag_columns', [])
        tag_kind = self.config.get('tag_kind', None)

        if not delimiter:
            return Response(error=SteamshipError(
                message="An empty delimiter was found.",
                suggestion="Please set the delimiter field of your Plugin Instance configuration to a non-empty value."
            ))

        if not escapechar:
            return Response(error=SteamshipError(
                message="An empty escapechar was found.",
                suggestion="Please set the escapechar field of your Plugin Instance configuration to a non-empty value."
            ))

        if not quotechar:
            return Response(error=SteamshipError(
                message="An empty quotechar was found.",
                suggestion="Please set the quotechar field of your Plugin Instance configuration to a non-empty value."
            ))

        if len(quotechar) > 1:
            return Response(error=SteamshipError(message="quotechar should be a single character."))
        if len(escapechar) > 1:
            return Response(error=SteamshipError(message="escapechar should be a single character."))

        if not text_column:
            return Response(error=SteamshipError(
                message="No text_column was found.",
                suggestion="Please set the text_column field of your Plugin Instance configuration to a non-empty value."
            ))

        reader = csv.DictReader(
            io.StringIO(request.data.data),
            delimiter=delimiter,
            quotechar=quotechar,
            escapechar=escapechar,
            skipinitialspace=skipinitialspace
        )

        file = File(blocks=[])
        for row in reader:
            text = row.get(text_column, None)
            if text:
                text = text.replace(newline, '\n')
                block = Block.CreateRequest(text=text, tags=[])
                for tag_column in tag_columns:
                    tag_name = row.get(tag_column, None)
                    if tag_name:
                        tag_name = tag_name.replace(newline, '\n')
                        block.tags.append(Tag.CreateRequest(kind=tag_kind, name=tag_name))
                file.blocks.append(block)

        return PluginResponse(data=BlockAndTagPluginOutput(file=file))

    @post('convert')
    def convert(self, **kwargs) -> Response:
        """App endpoint for our plugin.

        The `run` method above implements the Plugin interface for a Converter.
        This `convert` method exposes it over an HTTP endpoint as a Steamship App.

        When developing your own plugin, you can almost always leave the below code unchanged.
        """
        convertRequest = Converter.parse_request(request=kwargs)
        convertResponse = self.run(convertRequest)
        return Converter.response_to_dict(convertResponse)


handler = create_handler(CsvBlockifierPlugin)
