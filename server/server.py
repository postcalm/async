from aiohttp import web
from aiohttp.web import (
    Response, Request, Application, RouteTableDef
)


class Server:

    route: RouteTableDef = RouteTableDef()

    def __init__(self):
        self.host = "localhost"
        self.port = 8080

    @route.get('/')
    async def echo(self) -> Response:
        return Response(text="Hello")

    # если routes используется как декоратор,
    # то метод первым аргументом должен принимать сам request
    @staticmethod
    @route.get('/{name}')
    async def get_name(request: Request) -> Response:
        return Response(text=f"Hello, {request.match_info.get('name')}")

    async def server(self):
        app = Application()
        app.add_routes(self.route)
        return app

    def run(self):
        web.run_app(self.server(), host=self.host, port=self.port)
