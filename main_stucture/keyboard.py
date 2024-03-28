from aiogram import types


def admin_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=5)
    keyboard.add(types.InlineKeyboardButton("Add config", callback_data="add"))
    keyboard.add(types.InlineKeyboardButton("Remove config", callback_data="remove"))
    keyboard.add(types.InlineKeyboardButton("List of clients", callback_data="list"))
    keyboard.add(types.InlineKeyboardButton("Config + QR-code", callback_data="config+qr"))
    keyboard.add(types.InlineKeyboardButton("Get user password", callback_data="password"))
    return keyboard
