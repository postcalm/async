from aiohttp.web import Response
from server.handlers.base import BaseView
from server.storage import Storage


class ArtistView(BaseView):

    URL_PATH: str = "/api/music/{artist}"
    storage: Storage = Storage()

    async def post(self):
        artist = self.request.match_info.get("artist")
        self.storage.update({artist: {}})
        self.storage.write()
        return Response(text="Added artist")

    async def get(self):
        artist = self.request.match_info.get("artist")
        self.storage.read()

