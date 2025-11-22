
import logging

from aiogram import Bot, Dispatcher
from django.apps import AppConfig
from core import config

logger = logging.getLogger(__name__)


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    bot: Bot = None
    dp: Dispatcher = None

    def ready(self):
        """Initialize bot and dispatcher when Django starts"""
        if not BotConfig.bot:
            BotConfig.bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
            BotConfig.dp = Dispatcher()

            from bot.handlers import menu
            BotConfig.dp.include_router(menu.router)
