from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

REGIONS = [
    'Toshkent', 'Andijon',
    'Farg\'ona', 'Buxoro',
    'Marg\'ilon', 'Nukus',
    'Chirchiq', 'Qo\'qon'
]

def regions_keyboard():
    rows = []
    row = []
    for region in REGIONS:
        row.append(KeyboardButton(text=region))
        if len(row) == 2:
            rows.append(row)
            row = []

    keyboard = ReplyKeyboardMarkup(keyboard=rows, one_time_keyboard=True, resize_keyboard=True)
    return keyboard


