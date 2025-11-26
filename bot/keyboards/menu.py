from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from django.utils.translation import gettext as _

MENU = [
    _("🛍 Buyurtma berish"),
    _("📖 Buyurtmalar tarixi"),
    _("⚙️Sozlash ℹ️ Ma'lumotlar"),
    _("🔥 Aksiya"),
    _("🙋🏻‍♂️ Jamoamizga qo'shiling"),
    _("🙋☎️ Les Ailes bilan aloqa")
]

def menu_keyboard():
    rows = []
    row = []
    for index, menu_item in enumerate(MENU):
        row.append(KeyboardButton(text=menu_item))
        if index in (0, 1) or len(row) == 2:
            rows.append(row)
            row = []
    keyboard = ReplyKeyboardMarkup(keyboard=rows, one_time_keyboard=True, resize_keyboard=True)
    return keyboard