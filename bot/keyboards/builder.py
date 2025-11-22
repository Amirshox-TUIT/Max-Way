from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def db_keyboard(objects):
    rows = []
    row = []
    for obj in objects:
        row.append(KeyboardButton(text=obj.title))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    keyboard = ReplyKeyboardMarkup(keyboard=rows, one_time_keyboard=True, resize_keyboard=True)
    return keyboard
