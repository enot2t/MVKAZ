from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from app.tgbot.keyboards.users_board import event_board, main_user_board
from app.infrastructure.database.database.db import DB
from app.models.basemodels import UsersModel, UserRole
import requests
from datetime import datetime

commands_router = Router()


@commands_router.message(Command(commands='start'))
async def proccess_start_command(message: Message, db: DB) -> None:
    user_record: UsersModel | None = await db.users.get_user_record(user_id=message.from_user.id)
    if user_record is None:
        await db.users.add(
            user_id=message.from_user.id,
            role=UserRole.USER,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        )
    await message.answer(text='Привет!\nЭто event бот.\nУправляй своими событиями.',
                         reply_markup=main_user_board())


@commands_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        'Бот-помощник\n'
        'Помогает отслеживать события'
    )

@commands_router.message(F.text == 'События 📆',)
async def process_event_command(message: Message):
    await message.delete()
    await message.answer(
        'Управляй своими событиями.', reply_markup=event_board()
    )

@commands_router.message(F.text == 'Погода 🌞',)
async def process_weather_command(message: Message):
    await message.delete()
    def timestamp_to_date(timestamp):
        return datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y")
    weather = main_weather()
    # Парсинг текущей погоды
    current = weather["current_observation"]
    location = weather["location"]

    await message.answer(
        f"Город: {location['city']}, {location['country']}\n"
        f"Дата и время: {timestamp_to_date(current['pubDate'])}\n"
        f"Температура: {current['condition']['temperature']}°C\n"
        f"Состояние: {current['condition']['text']}\n"
        f"Ветер: {current['wind']['speed']} км/ч, направление: {current['wind']['direction']}\n"
        f"Влажность: {current['atmosphere']['humidity']}%\n"
        f"Видимость: {current['atmosphere']['visibility']} км\n"
        f"Давление: {current['atmosphere']['pressure']} мбар\n"
        f"Восход: {current['astronomy']['sunrise']}\n"
        f"Закат: {current['astronomy']['sunset']}\n"
    )


@commands_router.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy'
        )

def get_weather(location):
    url = f"https://yahoo-weather5.p.rapidapi.com/weather?location={location}&format=json&u=f"
    headers = {
        "x-rapidapi-host": "yahoo-weather5.p.rapidapi.com",
        "x-rapidapi-key": "f693aebe6emsh24b20d5277b40d4p1dccaajsn867936a8eb25"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

def main_weather():
    location = "Moscow"
    weather_data = get_weather(location)
    return weather_data