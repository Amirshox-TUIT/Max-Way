from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

SETTINGS = [
    "Ismni o'zgartirish",
    "Raqamni o'zgartirish",
    "Shaharni o'zgartirish",
    "Tilni o'zgartirish",
    "Filallar haqida ma'lumotlar",
    "Ommaviy taklif"
]

def settings_keyboard():
    rows = []
    row = []
    for setting in SETTINGS:
        row.append(KeyboardButton(text=setting))
        if len(row) == 2:
            rows.append(row)
            row = []

    rows.append([KeyboardButton(text="⬅️ Ortga")])
    return ReplyKeyboardMarkup(keyboard=rows, one_time_keyboard=True, resize_keyboard=True)
