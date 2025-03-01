from datetime import datetime, date
from psycopg import AsyncConnection, AsyncCursor
from app.models.basemodels import EventModel


class _EventDB:
    __tablename__ = 'events'

    def __init__(self, connection: AsyncConnection):
        self.connection = connection

    async def add(
            self,
            user_id: int,
            start_dt: date,
            end_dt: date,
            name: str,
            mode: str,
            place: str,
            description: str,
            duration: int
    ) -> None:
        await self.connection.execute('''
            INSERT INTO events(user_id, start_dt, end_dt, name, mode, place, description, duration)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
        ''', (user_id, start_dt, end_dt, name, mode, place, description, duration)
        )

    async def get_event(self, *, user_id: int) -> EventModel | None:
        cursor: AsyncCursor = await self.connection.execute('''
            SELECT  created,
                    user_id,
                    start_dt,
                    end_dt,
                    name,
                    mode,
                    place,
                    description,
                    duration
            FROM events
            WHERE events.user_id = %s
            ORDER BY id DESC
            LIMIT 1
        ''', (user_id, )
        )
        data = await cursor.fetchone()
        return EventModel(*data) if data else None

    async def load_events(self, *, user_id: int) -> list[EventModel] | None:
        cursor: AsyncCursor = await self.connection.execute('''
            SELECT start_dt,
                    end_dt,
                    name,
                    place,
                    description
                    --, duration
            FROM events
            WHERE events.user_id = %s
            ORDER BY id DESC
            --LIMIT 5
        ''', (user_id, )
        )
        data = await cursor.fetchall()  # Получаем все строки
        return [row for row in data] if data else None
