import unittest
from unittest.mock import patch
import os
from emoji_save import read_emojis, create_output_dir, download


class r:
    content = 'Test_string'


class TestEmojiSave(unittest.TestCase):
    test_dir = '.test'

    def setUp(self):
        self.emojis = {
            "ok": "true",
            "emoji": {
                "foo": "https://bar",
                }
            }

        if not os.path.exists(self.test_dir):
            os.mkdir(self.test_dir)

    def test_read_emojis(self):
        emojis = read_emojis(self.emojis)
        self.assertEqual(emojis, [('foo', 'https://bar'), ])

    def test_create_output_dir(self):
        self.assertFalse(create_output_dir(self.test_dir))

    @patch('emoji_save.requests.get')
    def test_download(self, mock_get):

        mock_get.return_value = r()
        emojis = read_emojis(self.emojis)
        [download(emoji, self.test_dir) for emoji in emojis]

    def tearDown(self):
        if os.path.exists(self.test_dir):
            if os.path.exists(self.test_dir + '/' + 'foo'):
                os.remove(self.test_dir + '/' + 'foo')
            os.rmdir(self.test_dir)


if __name__ == '__main__':
    unittest.main()
