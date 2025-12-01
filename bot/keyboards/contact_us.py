from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _, activate


def contact_us_keyboard(language_code="uz"):
    activate(language_code)
    CONTACT_US = [
        "💬 " + _("Biz bilan aloqaga chiqing"),
        "✍️ " + _("Fikr bildirish")
    ]
    return ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=CONTACT_US[0]), KeyboardButton(text=CONTACT_US[1])],
        [KeyboardButton(text="⬅️ " + _("Ortga"))]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)