from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text="📨Ovoz berish")
        ],
        [
            KeyboardButton(text="💰Balans"),
            KeyboardButton(text="💸Pul ishlash")
        ],
        [
            KeyboardButton(text="🧮Statistika")
        ]
    ], resize_keyboard=True
)

bekor = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌Bekor qilish")
        ]
    ], resize_keyboard=True
)