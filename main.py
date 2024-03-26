import asyncio
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, Dispatcher
from aiogram.types.bot_command import BotCommand
from data_base.redis_conn import storage

from admin.admin_commands import register_handlers_admin
from user_commands import register_handlers_commands
from admin import config

# Set the log level for debugging.
logging.basicConfig(level=logging.INFO)


bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Start!"),
        BotCommand(command="/get_wg_configuration", description="Get WG configuration"),
        BotCommand(command="/show_my_configurations", description="Lisf of your configs"),
    ]
    await bot.set_my_commands(commands)

async def main():
    register_handlers_admin(dp)
    register_handlers_commands(dp)
    await set_commands(bot)
    await dp.start_polling()


if __name__ == '__main__':
    dp.middleware.setup(LoggingMiddleware())
    asyncio.run(main())
