from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def ovoz_ber(url):
    ovoz = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📨Ovoz berish", url=url)
            ],
            [
                InlineKeyboardButton(text="➕Ovoz berdim", callback_data="ovoz_berdim")
            ],
            [
                InlineKeyboardButton(text="◀️Ortga", callback_data="ortga")
            ]
        ]
    )
    
    return ovoz