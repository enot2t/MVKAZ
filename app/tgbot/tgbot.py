import asyncio
import psycopg_pool
import logging
import sys
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from aiogram.fsm.storage.memory import MemoryStorage

from app.infrastructure.database.utils.connect_to_pg import get_pg_pool
from app.tgbot.handlers.commands import commands_router
from app.tgbot.handlers.simple_button import simple_router
from app.tgbot.handlers.FSMF_stage import event_router
from app.middlewares.database import DataBaseMiddleware
from app.tgbot.keyboards.main_menu import set_main_menu
from config.config import settings

if sys.platform.startswith("win") or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting bot")

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode(settings.bot.parse_mode)
            )
    )
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    await set_main_menu(bot)

    logger.info("Including routers")
    dp.include_routers(event_router, commands_router)

    dp.update.middleware(DataBaseMiddleware())

    db_pool: psycopg_pool.AsyncConnectionPool = await get_pg_pool(
        db_name=settings.postgres.name,
        host=settings.postgres.host,
        port=settings.postgres.port,
        user=settings.postgres_user,
        password=settings.postgres_password,
    )

    # Launch polling and delayed message consumer
    try:
        await asyncio.gather(dp.start_polling(bot, _db_pool=db_pool))

    except Exception as e:
        logger.exception(e)
    finally:
        await db_pool.close()
        logger.info('Connection to Postgres closed')