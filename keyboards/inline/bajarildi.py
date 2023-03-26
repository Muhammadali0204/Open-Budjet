from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def bajarildi(data):
    keyboard1 = InlineKeyboardMarkup(
        inline_keyboard=  [
            [
                InlineKeyboardButton(text="✅Bajarildi", callback_data=f"bajarildi:{data}")
            ],
        ],
    )
    
    return keyboard1