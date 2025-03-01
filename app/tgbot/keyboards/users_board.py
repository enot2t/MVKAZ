from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def simple_board() -> ReplyKeyboardMarkup:
    keyboard: list[list[KeyboardButton]] = [
        [KeyboardButton(text='Кошки')],
        [KeyboardButton(text='Собаки')]
        ]

    # Создаем объект клавиатуры, добавляя в него кнопки
    my_keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

    return my_keyboard


def event_board() -> ReplyKeyboardMarkup:
    keyboard: list[list[KeyboardButton]] = [
        [KeyboardButton(text='Внести событие')],
        [KeyboardButton(text='Посмотреть события')]
        ]

    # Создаем объект клавиатуры, добавляя в него кнопки
    my_keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

    return my_keyboard


def main_user_board() -> ReplyKeyboardMarkup:

    keyboard: list[list[KeyboardButton]] = [
        [KeyboardButton(text='События 📆')],
        [KeyboardButton(text='Погода 🌞')]
        ]

    # Создаем объект клавиатуры, добавляя в него кнопки
    my_keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

    return my_keyboard
