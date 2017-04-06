# Python 3.6 only
import signal
import sys
import asyncio
import async_timeout
import aiohttp
import json
import os
import logging

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
client = aiohttp.ClientSession(loop=loop)


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def get_slack_emojis(client, emojis):
    for k, v in emojis['emoji'].items():
        logging.info('Downloading {}...'.format(k))
        data = await get_file(client, v)
        with open('output2/{}'.format(k), 'w') as f:
            f.write(data)


def signal_handler(signal, frame):
    loop.stop()
    client.close()
    sys.exit(0)


if __name__ == '__main__':
    with open('emojis.json') as f:
        emojis = json.load(f)

    if not os.path.exists('output2'):
        os.makedirs('output2')

    signal.signal(signal.SIGINT, signal_handler)

    asyncio.ensure_future(get_slack_emojis(client=client, emojis=emojis))
    loop.run_forever()
