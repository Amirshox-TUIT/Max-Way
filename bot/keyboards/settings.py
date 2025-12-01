from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from django.utils.translation import gettext as _, activate


def settings_keyboard(language_code="uz"):
    activate(language_code)
    SETTINGS = [
        _("Ismni o'zgartirish"),
        _("Raqamni o'zgartirish"),
        _("Shaharni o'zgartirish"),
        _("Tilni o'zgartirish"),
        _("Filallar haqida ma'lumotlar"),
        _("Ommaviy taklif")
    ]
    rows = []
    row = []
    for setting in SETTINGS:
        row.append(KeyboardButton(text=setting))
        if len(row) == 2:
            rows.append(row)
            row = []

    rows.append([KeyboardButton(text="⬅️ " + _("Ortga"))])
    return ReplyKeyboardMarkup(keyboard=rows, one_time_keyboard=True, resize_keyboard=True)
