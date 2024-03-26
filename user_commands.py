import asyncio
import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types
from data_base.redis_conn import storage
from pass_for_user import generate_password
from class_user import User
from generate_send_qr import generate_wg_config, send_all_qr_codes_and_configs, send_last_qr_code_and_config
from admin import config

bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()

logging.basicConfig(level=logging.INFO)


class User_commands(StatesGroup):
    password_to_get_conf = State()


async def send_welcome(message: types.Message):
    username = message.from_user.username
    cid = message.chat.id
    password = generate_password()
    if User(username).is_user():
        await message.answer("Hello. :)")
    else:
        User(username).create_new_user(password, cid)
        await message.answer("Hi! This is VpnBot, which provides Wireguard configurations."
                             " Use menu.")

async def enter_password(message: types.Message):
    await message.answer("Enter the password to access the WireGuard configuration:")
    await User_commands.password_to_get_conf.set()


async def get_new_config(message: types.Message, state: FSMContext):
    username = message.from_user.username
    cid = message.chat.id
    generate_wg_config(username)
    await message.answer("Your WG_configuration:")
    await send_last_qr_code_and_config(username, cid)
    User(username).create_new_password()
    await state.finish()


async def show_configs(message:types.Message):
    username = message.from_user.username
    cid = message.chat.id
    await message.answer("List of your WG_configurations:")
    await send_all_qr_codes_and_configs(username, cid)


async def wrong_password(message: types.Message):
    await message.answer("Wrong password: Try one more time.")


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands="start", state="*")
    dp.register_message_handler(enter_password, commands="get_wg_configuration", state="*")
    dp.register_message_handler(get_new_config,
                                lambda message: message.text == User(message.from_user.username).get_user_password(),
                                state=User_commands.password_to_get_conf)

    dp.register_message_handler(show_configs, commands="show_my_configurations", state="*")
    dp.register_message_handler(wrong_password,
                                lambda message: message.text != User(message.from_user.username).get_user_password(),
                                state=User_commands.password_to_get_conf)
