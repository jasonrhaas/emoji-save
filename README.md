# emoji-save
Save all those custom slack emojis!

## Requirements
- Python 3.6+
- Slack Legacy Token

## Usage

1. [Token](https://api.slack.com/custom-integrations/legacy-tokens) -- Log into your Slack Team and make sure that you have generated a test token.
2. [Emoji.list](https://api.slack.com/methods/emoji.list/test) -- Use this endpoint to get a list of custom Slack emojis.
3. Save this to a `emojis.json` file in the top level folder.


Now you are ready to download some emojis.  There are few different ways you can go in order of download speed.

To see full options run `python3 emoji_save.py --help`

- Synchronous, single process.  `python3 emoji_save.py`
- Synchronous, multi process.  `python3 emoji_save.py -p 4`  (where p is number of processes)
- TODO: Asynchronous, single process
- TODO: Asynchronous, multi process

## Testing

Test are written with the standard library `unittest` suite.

`python3 test.py` to run the tests.
