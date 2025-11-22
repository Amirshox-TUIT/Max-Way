from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

DElIVERY_TYPE = [
    "🏃 Olib ketish",
    "🚙 Yetkazib berish"
]

def delivery_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=DElIVERY_TYPE[0]), KeyboardButton(text=DElIVERY_TYPE[1])],
            [KeyboardButton(text="⬅️ Ortga")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )