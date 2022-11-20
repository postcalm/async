import asyncio
import sys

from aiohttp import ClientSession


class Client:

    def __init__(self):
        self.host = "localhost"
        self.port = 8080

    async def start(self):
        while True:
            request = input()
            match request:
                case ['echo']:
                    await self.start_session()
                case _:
                    await self.start_session(request)

    async def start_session(self, request=""):
        async with ClientSession() as session:
            async with session.get(f'http://{self.host}:{self.port}/{request}') as response:
                print(response.status)
                print(await response.text())

    def run(self):
        asyncio.run(self.start())
