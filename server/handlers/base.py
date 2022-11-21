from aiohttp.web_urldispatcher import View


class BaseView(View):

    URL_PATH: str
