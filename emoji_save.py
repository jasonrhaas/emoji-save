import requests
from requests.exceptions import InvalidSchema
import os
import json
from multiprocessing import Pool
from functools import partial
import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.INFO)


def read_emojis(emojis):
    """ Returns a dictionary of emojis in the format of name: url. """

    items = []
    for k, v in emojis['emoji'].items():
        if v.startswith('http'):
            items.append((k, v))

    return items


def create_output_dir(output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        return True
    return False


def download(emoji, output_dir):
    """ Emoji tuple. """
    name, url = emoji[0], emoji[1]
    try:
        logger.debug(f'Downloading {name}...')
        r = requests.get(url)
    except InvalidSchema:
        logger.warning(f'Skipping {name}')
    else:
        # with open(output_dir + '/' + name, 'w') as f:
        #     content = str(r.content)
        #     f.write(content)
        return name, str(r.content)


def write(content, output_dir):
    fname, data = content[0], content[1]
    with open(output_dir + '/' + fname, 'w') as f:
        f.write(content)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Emoji save CLI.')
    parser.add_argument('-p', '--processes', default=0, help='Number of processes to use.')
    parser.add_argument('-f', '--folder', default='output', help='Download folder.')
    parser.add_argument('-e', '--emoji', default='emojis.json', help='Emoji json file.')

    args = parser.parse_args()

    create_output_dir(args.folder)
    with open(args.emoji) as f:
        emoji_dict = json.load(f)

    emojis = read_emojis(emoji_dict)

    if args.processes:
        logger.warning(f'Using {args.processes} processes')
        m_download = partial(download, output_dir=args.folder)
        with Pool(processes=int(args.processes)) as pool:
            content = pool.map(m_download, emojis)
            m_write = partial(write, output_dir=args.folder)
            pool.map(m_write, content)
    else:
        [download(emoji, args.folder) for emoji in emojis]
