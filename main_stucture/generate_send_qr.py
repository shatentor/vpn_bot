import asyncio
import logging
import subprocess
from aiogram import Bot, Dispatcher, types
import os

from main_stucture.class_user import User
from admin import config

# Set the log level for debugging.
logging.basicConfig(level=logging.INFO)


bot = Bot(token=config.token)
dp = Dispatcher(bot)
loop = asyncio.get_event_loop()


def delete_qr(username, number_of_cofig):
    if os.path.exists(f"{username}_{number_of_cofig}-qr.png"):
        os.remove(f"{username}_{number_of_cofig}-qr.png")


def generate_wg_config(username):
    number_of_configs = User(username).get_number_of_configs()
    # Generating WireGuard configuration using PiVPN and the username.
    command = f"sudo pivpn add --name {username}_{number_of_configs+1}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    User(username).set_date_config(str(number_of_configs+1))
    User(username).plus_config_number()
    return result.stdout


async def send_all_qr_codes_and_configs(username, chat_id):
    # Path to the WireGuard configuration file.
    number_of_configs = User(username).get_number_of_configs()

    try:
        for number in range(1, number_of_configs+1):
            wg_config_path = f'/home/nikita/configs/{username}_{number}.conf'
            # Checking the file's existence
            if not os.path.exists(wg_config_path):
                return

        # Creating a QR code for the WireGuard configuration.
            config_input_file = types.InputFile(wg_config_path)
            command = f"qrencode -t png -o {username}_{number}-qr.png -r {wg_config_path}"
            subprocess.run(command, shell=True, capture_output=True, text=True)

            await bot.send_document(chat_id, config_input_file)
            await bot.send_photo(chat_id, types.InputFile(f'{username}_{number}-qr.png'))
            delete_qr(username, number)
    except TypeError:
        await bot.send_message(chat_id, "User has no configs.")

async def send_last_qr_code_and_config(username, chat_id):
    number = User(username).get_number_of_configs()
    wg_config_path = f'/home/nikita/configs/{username}_{number}.conf'
    # Checking the file's existence
    if not os.path.exists(wg_config_path):
        return

    # Creating a QR code for the WireGuard configuration.
    config_input_file = types.InputFile(wg_config_path)
    command = f"qrencode -t png -o {username}_{number}-qr.png -r {wg_config_path}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    try:
        await bot.send_document(chat_id, config_input_file)
        await bot.send_photo(chat_id, types.InputFile(f'{username}_{number}-qr.png'))
        delete_qr(username, number)
    except TypeError:
        await bot.send_message(chat_id, "User has no configs.")
