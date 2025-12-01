from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _, activate


def location_keyboard(language_code="uz"):
    activate(language_code)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("Bu yerda buyurtma berish") + " 🌐"),
                KeyboardButton(text=_("Filialni tanlang"))
            ],
            [
                KeyboardButton(text="📍 " + _("Eng yaqin filialni aniqlash")),
                KeyboardButton(text="⬅️ " + _("Ortga"))
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard