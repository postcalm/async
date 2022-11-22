from sqlalchemy import (
    Column, Table, ForeignKey, ForeignKeyConstraint, Integer, String,
    MetaData
)

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),

    # Именование индексов
    'ix': 'ix__%(table_name)s__%(all_column_names)s',

    # Именование уникальных индексов
    'uq': 'uq__%(table_name)s__%(all_column_names)s',

    # Именование CHECK-constraint-ов
    'ck': 'ck__%(table_name)s__%(constraint_name)s',

    # Именование внешних ключей
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',

    # Именование первичных ключей
    'pk': 'pk__%(table_name)s'
}
metadata = MetaData(naming_convention=convention)

imports_table = Table(
    'imports',
    metadata,
    Column('import_id', Integer, primary_key=True)
)

artists_table = Table(
    'artists',
    metadata,
    Column('import_id', Integer, ForeignKey('imports.import_id'), primary_key=True),
    Column('artist_id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('genre', String, nullable=False)
)

songs_table = Table(
    'songs',
    metadata,
    Column('import_id', Integer, primary_key=True),
    Column('song_id', Integer, primary_key=True),
    Column('artist_id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    ForeignKeyConstraint(
        ('import_id', 'artist_id'),
        ('artists.import_id', 'artists.artist_id'),
    ),
    ForeignKeyConstraint(
        ('import_id', 'song_id'),
        ('artists.import_id', 'artists.artist_id'),
    )
)
