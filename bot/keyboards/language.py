from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_language_keyboard():
    """Keyboard for language selection"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en"),
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
        ]
    ])
    return keyboard