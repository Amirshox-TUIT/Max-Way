from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from django.utils.translation import gettext as _, activate


def db_keyboard(objects, language_code="uz"):
    activate(language_code)
    rows = []
    row = [KeyboardButton(text="⬅️ Ortga")]
    for obj in objects:
        if hasattr(obj, 'title'):
            row.append(KeyboardButton(text=obj.title))
        else:
            row.append(KeyboardButton(text=obj.name))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    keyboard = ReplyKeyboardMarkup(keyboard=rows, one_time_keyboard=True, resize_keyboard=True)
    return keyboard
