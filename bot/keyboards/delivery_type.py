from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _

DElIVERY_TYPE = [
    _("🏃 Olib ketish"),
    _("🚙 Yetkazib berish")
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