# CSV Blockfier - Steamship Plugin

In Steamship, a **Blockfier Plugin** converts bytes of data into Steamship's universal **Block Format**.

The CSV Blockifier converts a CSV file into tagged blocks of text, e.g. for use training and hosting a classifier.

For example, given the file:

```tsv
Utterance                     Category          Account Source
"Hi there, how's it going?"   Greeting          0012    log3.txt
"Can I get a coupon?"         Coupon            0013    log3.txt
"What's your address?"        Request-Address   0013    log3.txt
```

The CSV Blockfier can transform this into a file with blocks:

* Hi there, how's it going?
* Can I get a coupon?
* What's your address?

And with the `Category` field acting as a tag on the text of each appropriate block.

## Using

Once deployed, your Blockfier Plugin can be referenced by the handle in your `steamship.json` file.

```python
from steamship import Steamship, BlockTypes

MY_PLUGIN_HANDLE = ".. fill this out .."

client = Steamship()
file = client.create_file(file="./test_data/king_speech.txt")
file.convert(plugin=MY_PLUGIN_HANDLE).wait()
file.query(blockType=BlockTypes.Paragraph).wait().data
```

## Developing

This plugin is hosted and ready to use without any development on your part. 
But if you wish to contribute to it or use it as a starting place for your own plugin, see DEVELOPING.md.

