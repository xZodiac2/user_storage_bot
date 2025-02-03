from res import Actions
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=Actions.INSERT_USER.value)],
    [KeyboardButton(text=Actions.INSERT_RESUME.value)],
    [KeyboardButton(text=Actions.GET_ALL_USERS.value)]
])
