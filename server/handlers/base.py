from asyncpg import Pool
from aiohttp.web_urldispatcher import View


class BaseView(View):

    URL_PATH: str

    def pg(self):
        return self.request.app['pg']
