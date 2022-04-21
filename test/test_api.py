from steamship.plugin.service import PluginRequest
from steamship.plugin.inputs.raw_data_plugin_input import RawDataPluginInput
from src.api import CsvBlockifierPlugin
import os

__copyright__ = "Steamship"
__license__ = "MIT"

TEST_HEADERS = [
    "ID",
    "Text",
    "Tag",
    "Something"
]

TEST_DATA = [
    ["Hi there", "A", None],
    ["Hi there" ,"B", "Foo"],
    ['Hi "there', "C", "Bar"],
    ["Hi \nthere", "D", "Foo"],
    ["Hi \nthere", None, None]
]

def _read_test_file(filename: str) -> str:
    folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(folder, '..', 'test_data', filename), 'r') as f:
        return f.read()

def _check_normal_response(file, tag1: bool, tag2: bool, kind: str):
    assert (file is not None)
    assert (file.blocks is not None)
    assert (len(file.blocks) == 5)
    for i in range(len(TEST_DATA)):
        assert(file.blocks[i].text == TEST_DATA[i][0])
        expect_tags = []
        if tag1 and TEST_DATA[i][1]:
            expect_tags.append(TEST_DATA[i][1])
        if tag2 and TEST_DATA[i][2]:
            expect_tags.append(TEST_DATA[i][2])
        if len(expect_tags) > 0:
            assert(file.blocks[i].tags is not None)
            assert(len(file.blocks[i].tags) == len(expect_tags))
            had_tags = map(lambda t: (t.kind, t.name), file.blocks[i].tags)
            for tag in expect_tags:
                assert (kind, tag) in had_tags
        else:
            assert(file.blocks[i].tags is not None)
            assert(len(file.blocks[i].tags) == 0)

def test_variation(tag1: bool, tag2: bool, kind: str, dilem: str):
    if dilem == "csv":
        filename = "normal.csv"
        dilemeter = None # Test the default
    elif dilem == "tsv":
        filename = "normal.tsv"
        dilemeter = "\t"
    else:
        assert("Error: unknown dilem value" == True)

    tag_cols = []
    if tag1:
        tag_cols.append(TEST_HEADERS[2])
    if tag2:
        tag_cols.append(TEST_HEADERS[3])

    converter = CsvBlockifierPlugin(config=dict(
        delimiter=dilemeter,
        text_column=TEST_HEADERS[1],
        tag_columns=tag_cols,
        tag_kind=kind
    ))
    data = _read_test_file(filename)
    request = PluginRequest(data=RawDataPluginInput(data=data))
    response = converter.run(request)

    assert(response.error is None)
    assert(response.data is not None)
    _check_normal_response(response.data.file, tag1=tag1, tag2=tag2, kind=kind)


def test_basic_variations():
    for tag1 in [True, False]:
        for tag2 in [True, False]:
            for kind in [None, "SomeKind"]:
                for dilemeter in ["csv", "tsv"]:
                    print(tag1, tag2, kind, dilemeter)
                    test_variation(tag1, tag2, kind, dilemeter)

