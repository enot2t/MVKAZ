from datetime import datetime
from aiogram import types
from aiogram.filters import BaseFilter
from aiogram.types import Message


class DateFilter(BaseFilter):
    def __init__(self, stringer: str) -> None:
        self.stringer = stringer

    async def __call__(self, message: Message) -> bool:
        try:
            datetime.strptime(self.stringer.text, '%d-%m-%Y')
            return True
        except:
            return False
