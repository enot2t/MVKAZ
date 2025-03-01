from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def select_mode_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Постоянное', callback_data='permanent')],
            [InlineKeyboardButton(text='Временное',  callback_data='temporary')]
            ])