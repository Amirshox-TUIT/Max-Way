from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _, activate


def delivery_keyboard(language_code="uz"):
    activate(language_code)
    DElIVERY_TYPE = [
        "🏃 " + _("Olib ketish"),
        "🚙 " + _("Yetkazib berish")
    ]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=DElIVERY_TYPE[0]), KeyboardButton(text=DElIVERY_TYPE[1])],
            [KeyboardButton(text="⬅️ " + _("Ortga"))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )