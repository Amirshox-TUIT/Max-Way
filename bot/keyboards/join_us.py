from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.utils.translation import gettext as _, activate


def join_us_inline_keyboard(language_code="uz"):
    activate(language_code)
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=_("O'tish"), url="https://github.com/Amirshox-TUIT")]
])