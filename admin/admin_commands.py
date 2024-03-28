import asyncio
import logging
import subprocess
import os
import re
from aiogram.utils.exceptions import MessageTextIsEmpty
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from main_stucture.keyboard import admin_keyboard
from data_base.redis_conn import storage
from main_stucture.generate_send_qr import send_all_qr_codes_and_configs
from admin.config import token
from main_stucture.class_user import User


bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)
loop = asyncio.get_event_loop()


logging.basicConfig(level=logging.INFO)


class AdminCommands(StatesGroup):
    add = State()
    remove = State()
    qr_code = State()
    password = State()


def is_admin(username):
    if username == 'admin':
        return True
    else:
        return False


async def admin_func(message: types.Message):
    username = message.from_user.username
    cid = message.chat.id
    if is_admin(username):
        await bot.send_message(cid, "Select an action", reply_markup=admin_keyboard())
    else:
        await bot.send_message(cid, 'You are not admin! Do not joke with me')


async def add_config_func(call):
    await call.message.answer("Enter new config name:")
    await AdminCommands.add.set()


async def name_add_config(message: types.Message, state: FSMContext):
    command = f"pivpn add --name {message.text}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # Format the output for better readability
    output = f"Command Output:\n```\n{result.stdout}\n```\n"
    try:
        if result.stdout:
            await message.answer(output, parse_mode='Markdown')
        else:
            error_message = f"Error Output:\n```\n{result.stderr}\n```\n"
            await message.answer(error_message, parse_mode='Markdown')
    except MessageTextIsEmpty:
        error_message = f"Error Output:\n```\nEMPTY MESSAGE\n```\n"
        await message.answer(error_message, parse_mode='Markdown')

    await state.finish()


async def show_list_of_configs(call):
    message = call.message
    command = f"pivpn -l"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    out = result.stdout
    error = result.stderr
    if error:
        await message.answer(f"Error occurred:\n{error}")
        return
    #formating output
    lines = out.strip().split('\n')

    clients_info = [line.strip() for line in lines[3:-1]]

    # make beautiful print
    formatted_message = "List of clients:\n"
    for client_info in clients_info:
        match = re.match(r'(\S+)\s+(\S+)\s+(.+)', client_info.strip())
        if match:
            client_name, _, creation_date = match.groups()
            formatted_message += f"👤 {client_name} - {creation_date}"
            if "Disabled" in client_info:
                formatted_message += " (Disabled)"
            formatted_message += "\n"

    await message.answer(formatted_message)


async def remove_config_func(call):
    await call.message.answer("Who to delete?")
    await AdminCommands.remove.set()


async def name_remove_config(message: types.Message, state: FSMContext):
    command = f"pivpn -r {message.text}"
    # Confirmation
    confirmation_input = "y"
    # Command transmission
    command = f'echo "{confirmation_input}" | {command}'

    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
    # Format the output for better readability
    output = f"Command Output:\n```\n{result.stdout}\n```\n"
    try:
        if result.stdout:
            await message.answer(output, parse_mode='Markdown')
        else:
            error_message = f"Error Output:\n```\n{result.stderr}\n```\n"
            await message.answer(error_message, parse_mode='Markdown')

    except MessageTextIsEmpty:
        error_message = f"Error Output:\n```\nEMPTY MESSAGE\n```\n"
        await message.answer(error_message, parse_mode='Markdown')

    await state.finish()


async def qr_code_func(call):
    await call.message.answer("Whose QR to send?")
    await AdminCommands.qr_code.set()


async def qr_code_name(message: types.Message, state: FSMContext):
    if User(message.text).is_user():
        await send_all_qr_codes_and_configs(message.text, message.chat.id)
    else:
        wg_config_path = f'/home/nikita/configs/{message.text}.conf'
        # Checking the file's existence
        if not os.path.exists(wg_config_path):
            await message.answer("This file does not exists")

        # Creating a QR code for the WireGuard configuration.
        config_input_file = types.InputFile(wg_config_path)
        command = f"qrencode -t png -o {message.text}-qr.png -r {wg_config_path}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        try:
            await bot.send_document(message.chat.id, config_input_file)
            await bot.send_photo(message.chat.id, types.InputFile(f'{message.text}-qr.png'))
            if os.path.exists(f"{message.text}-qr.png"):
                os.remove(f"{message.text}-qr.png")
            if result.stderr:
                error_message = f"Error Output:\n```\n{result.stderr}\n```\n"
                await message.answer(error_message, parse_mode='Markdown')
        except MessageTextIsEmpty:
            error_message = f"Error Output:\n```\nEMPTY MESSAGE\n```\n"
            await message.answer(error_message, parse_mode='Markdown')


    await state.finish()


async def get_password(call):
    await call.message.answer("Whose password to send?")
    await AdminCommands.password.set()


async def name_for_password(message: types.Message, state: FSMContext):
    await message.answer(f"{User(message.text).get_user_password()}")
    await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_func, commands="admin", state="*")
    dp.register_callback_query_handler(add_config_func, lambda call: call.data == "add", state="*")
    dp.register_message_handler(name_add_config, state=AdminCommands.add)
    dp.register_callback_query_handler(show_list_of_configs, lambda call: call.data == "list", state="*")
    dp.register_callback_query_handler(remove_config_func, lambda call: call.data == "remove", state="*")
    dp.register_message_handler(name_remove_config, state=AdminCommands.remove)
    dp.register_callback_query_handler(qr_code_func, lambda call: call.data == "config+qr", state="*")
    dp.register_message_handler(qr_code_name, state=AdminCommands.qr_code)
    dp.register_callback_query_handler(get_password, lambda call: call.data == "password", state="*")
    dp.register_message_handler(name_for_password, state=AdminCommands.password)
