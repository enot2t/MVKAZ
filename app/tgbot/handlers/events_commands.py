from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from app.tgbot.keyboards.users_board import event_board, main_user_board
from app.infrastructure.database.database.db import DB
import pandas as pd
from datetime import datetime
from aiogram.types import Message, FSInputFile
from app.models.basemodels import EventModel
from app.tgbot.utils.file_management import get_pdf_path
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
import os

menu_events = Router()

@menu_events.message(F.text == 'Событие на дату 📅')
async def date_events(message: Message):
    await message.answer(text='Введите дату',
                         reply_markup=await SimpleCalendar().start_calendar())

@menu_events.message(F.text == 'Посмотреть все события')
async def show_events(message: Message, db: DB):

    event_load: EventModel | None = await db.events.load_events(user_id=message.from_user.id)
    columns = [
            "Дата начала",
            "Дата окончания",
            "Название события",
            "Время события",
            "Место проведения",
            "Описание"
        ]

    # Создание DataFrame
    df = pd.DataFrame(event_load, columns=columns)
    df_message = df[['Название события']]
    pdf_path = get_pdf_path(df)

    await message.answer(text=f"<pre>{df_message.to_string(index=False,header=False)}</pre>", parse_mode='HTML')
    # Отправка PDF-файла
    await message.answer_document(document=FSInputFile(pdf_path))

    # Удаление файла после отправки
    os.remove(pdf_path)

@menu_events.message(F.text == 'Назад ⬅️')
async def back_events(message: Message):
    await message.answer(text='Главное меню',
                         reply_markup=main_user_board())
