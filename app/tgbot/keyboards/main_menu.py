import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

logger = logging.getLogger(__name__)


async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command='/start',
                   description='Начало работы бота'),
        BotCommand(command='/help',
                   description='Описание возможностей бота')
    ]

    await bot.set_my_commands(main_menu_commands, scope=BotCommandScopeDefault())