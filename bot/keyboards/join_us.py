from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.utils.translation import gettext as _

join_us_inline_keyboard = (
    InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=_("O'tish"), url="https://github.com/Amirshox-TUIT")]
]))