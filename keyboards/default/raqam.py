from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

raqam = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text="📤Raqamimni yuborish", request_contact=True)
        ]
    ], resize_keyboard=True
)