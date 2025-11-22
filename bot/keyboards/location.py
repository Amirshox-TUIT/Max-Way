from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def location_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Bu yerda buyurtma berish 🌐"),
                KeyboardButton(text="Filialni tanlang")
            ],
            [
                KeyboardButton(text="📍Eng yaqin filialni aniqlash"),
                KeyboardButton(text="⬅️ Ortga")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard