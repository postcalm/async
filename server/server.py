import json
import os

from aiohttp import web
from aiohttp.web import (
    Response, Request, Application, RouteTableDef
)

from server.handlers import HANDLERS


class Server:

    app: Application

    def __init__(self):
        self.host = "localhost"
        self.port = 8080
        self.app = Application()

    @route.get('/get')
    async def echo(self) -> Response:
        return Response(text="Hello")

    # если routes используется как декоратор,
    # то метод первым аргументом должен принимать сам request
    @staticmethod
    @route.get('/get/{name}')
    async def get_name(request: Request) -> Response:
        return Response(text=f"Hello, {request.match_info.get('name')}")

    @staticmethod
    @route.post('/post/{name}')
    async def post_name(request: Request) -> Response:
        data = await request.json()
        with open('file.json', 'w') as f:
            json.dump(data, f, indent=2)
        return Response(text=f'Post request: {data}')

    @staticmethod
    @route.put('/put/{name}')
    async def put_name(request: Request):
        data: dict = await request.json()
        with open('file.json', 'r') as f:
            content: dict = json.load(f)
            content.update(data)
        with open('file.json', 'w') as f:
            json.dump(content, f, indent=2)
        return Response(text=f'Put request: {data}')

    @staticmethod
    @route.delete('/delete/{name}')
    async def delete_name(self, request: Request):
        data = await request.read()
        data = data.decode('utf8')
        with open('file.json', 'r') as f:
            content: dict = json.load(f)
        if data not in content:
            return Response(text=f"Not {data}")
        with open('file.json', 'w') as f:
            content.pop(data)
            json.dump(content, f, indent=2)
        return Response(text=f'Delete request: {data}')

    def register_handlers(self):
        for handler in HANDLERS:
            self.app.router.add_route('*', handler.URL_PATH, handler)

    def run(self):
        self.register_handlers()
        web.run_app(self.app, host=self.host, port=self.port)
