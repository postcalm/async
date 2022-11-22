from typing import Generator
from server.handlers.base import BaseView
from utils.utils import chunk_list
from aiohttp.web import Response
from http import HTTPStatus
from db.schema import imports_table, artists_table, songs_table


MAX_QUERY_ARGS = 32_767


class ImportsView(BaseView):

    URL_PATH: str = '/api'

    MAX_ARTISTS_PER_INSERT = MAX_QUERY_ARGS // len(artists_table.columns)
    MAX_SONGS_PER_INSERT = MAX_QUERY_ARGS // len(songs_table.columns)

    @classmethod
    def make_artists_table_rows(cls, artists, import_id) -> Generator:
        for artist in artists:
            yield {
                'import_id': import_id,
                'artist_id': artist['artist_id'],
                'name': artist['name'],
                'genre': artist['genre'],
            }

    def make_songs_table_rows(cls, artists, import_id) -> Generator:
        for artist in artists:
            for song_id in artist['songs']:
                yield {
                    'import_id': import_id,
                    'song_id': song_id,
                    'artist_id': artist['artist_id'],
                    'name': artist['name'],
                }

    async def post(self):
        async with self.pg.transaction() as conn:
            query = imports_table.insert().returning(imports_table.c.import_id)
            import_id = await conn.fetchval(query)

            artists = self.request['data']['artists']
            artist_rows = self.make_artists_table_rows(artists, import_id)
            songs_rows = self.make_songs_table_rows(artists, import_id)

            chunked_artists_rows = chunk_list(
                artist_rows,
                self.MAX_ARTISTS_PER_INSERT
            )
            chunked_songs_rows = chunk_list(
                songs_rows,
                self.MAX_SONGS_PER_INSERT
            )

            query = artists_table.insert()
            for chunk in chunked_artists_rows:
                await conn.execute(query.values(list(chunk)))

            query = songs_table.insert()
            for chunk in chunked_songs_rows:
                await conn.execute(query.values(list(chunk)))

        return Response(
            body={'data': {'import_id': import_id}},
            status=HTTPStatus.CREATED
        )
