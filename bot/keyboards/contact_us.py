from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _

CONTACT_US = [
    _("💬 Biz bilan aloqaga chiqing"),
    "✍️ Fikr bildirish"
]

contact_us_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=CONTACT_US[0]), KeyboardButton(text=CONTACT_US[1])],
        [KeyboardButton(text="⬅️ Ortga")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)