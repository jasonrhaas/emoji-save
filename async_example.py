#!/usr/local/bin/python3.6
import asyncio
from aiohttp import ClientSession
import logging

logging.basicConfig(level=logging.INFO)


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


async def run(emojis, output_dir):
    """ Download the emojis and save them to a file with the name of the dict key.

        :param dict emojis:  JSON response from the slack API containing the emoji info.
        :writes:  Files to output folder.
    """

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for key, value in emojis['emoji'].items():
            try:
                task = await asyncio.ensure_future(fetch(url=value, session=session))
            except:
                logging.warning(f'Skipping over {key}')
            else:
                async with open(output_dir + '/' + key, 'wb') as f:
                    logging.info(f'Writing out {key}')
                    f.write(task)


if __name__ == '__main__':
    import json

    with open('emojis.json') as f:
        emojis_obj = json.load(f)

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(emojis_obj, 'output2'))
    loop.run_until_complete(future)
