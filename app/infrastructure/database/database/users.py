import logging
from datetime import datetime
from psycopg import AsyncConnection, AsyncCursor
from app.models.basemodels import UserRole
from app.models.basemodels import UsersModel

logger = logging.getLogger(__name__)


class _UsersDB:
    __tablename__ = 'users'

    def __init__(self, connection: AsyncConnection):
        self.connection = connection

    async def add(
            self,
            user_id: int,
            role: UserRole,
            first_name: str,
            last_name: str,
            username: str
    ) -> None:
        await self.connection.execute('''
            INSERT INTO users(user_id, role, first_name, last_name, username)
            VALUES(%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
        ''', (user_id, role.value, first_name, last_name, username)
        )
        logger.info(
            "User added. db='%s', user_id=%d, date_time='%s', "
            "first_name='%s', last_name=%s, username=%s",
            self.__tablename__, user_id, datetime.now(),
            first_name, last_name, username
        )

    async def get_user_record(self, *, user_id: int) -> UsersModel | None:
        cursor: AsyncCursor = await self.connection.execute('''
            SELECT id,
                    user_id,
                    created,
                    role,
                    first_name,
                    last_name,
                    username
            FROM users
            WHERE users.user_id = %s
        ''', (user_id, )
        )
        data = await cursor.fetchone()
        return UsersModel(*data) if data else None