from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def simple_board():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton(
            text='Кнопка 1'
        ),
        KeyboardButton(
            text='Кнопка 2'
        )
    )
    return keyboard


BOT_TOKEN = '8186829020:AAHOFrIgn5Ed532QGC-ZRKtNE1gIVq_MnJQ'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands='start'))
async def proccess_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот\nНапиши мне что-то', reply_markup=simple_board())

@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь в ответ'
        'Я пришлю тебе твое сообщение'
    )

@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy'
        )


if __name__ == '__main__':
    dp.run_polling(bot)
