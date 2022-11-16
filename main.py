import os
import time
import platform
import functools
import asyncio
import aiohttp
from pathlib import Path
from aiohttp import ClientSession


URL = 'https://loremflickr.com/320/240'


# workaround использования aiohttp под windows
# https://github.com/aio-libs/aiohttp/issues/4324#issuecomment-733884349
def silence_event_loop_closed(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper


def write_image(data):
    folder = Path('jpeg')
    os.makedirs(folder, exist_ok=True)
    filename = 'file-{}.jpeg'.format(int(time.time() * 1000))
    with open(folder / filename, 'wb') as file:
        file.write(data)


async def fetch_content(url: str, session: ClientSession):
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        write_image(data)


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch_content(URL, session)) for _ in range(10)]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.proactor_events._ProactorBasePipeTransport.__del__ = silence_event_loop_closed(
            asyncio.proactor_events._ProactorBasePipeTransport.__del__
        )
        asyncio.run(main())
    elif platform.system() == 'Linux':
        asyncio.run(main())
