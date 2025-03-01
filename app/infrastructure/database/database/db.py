from psycopg import AsyncConnection

from app.infrastructure.database.database.users import _UsersDB
from app.infrastructure.database.database.events import _EventDB


class DB:
    def __init__(self, connection: AsyncConnection) -> None:
        self.users = _UsersDB(connection=connection)
        self.events = _EventDB(connection=connection)