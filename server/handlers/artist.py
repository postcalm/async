from aiohttp.web import Response
from server.handlers.base import BaseView
from server.storage import Storage


class ArtistView(BaseView):

    URL_PATH: str = "/api/music/{artist}"

    async def post(self):
        async with self.pg.transaction() as conn:
            ...

        return Response(text="Added artist")

    async def get(self):
        artist = self.request.match_info.get("artist")

