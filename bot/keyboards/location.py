from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _

def location_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Bu yerda buyurtma berish 🌐")),
                KeyboardButton(text=_("Filialni tanlang"))
            ],
            [
                KeyboardButton(text=_("📍Eng yaqin filialni aniqlash")),
                KeyboardButton(text="⬅️ Ortga")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard