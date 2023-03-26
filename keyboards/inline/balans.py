from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def balans_keyboard(data):

    balans = InlineKeyboardMarkup(
        row_width=1
    )
    
    balans.insert(InlineKeyboardButton(text="💰Pulni raqamimga yechish", callback_data="pul_yechish_raqam"))
    balans.insert(InlineKeyboardButton(text="💰Boshqa raqamga yechish", callback_data="pul_yechish_boshqa_raqam"))
    if data[4] != None:
        balans.insert(InlineKeyboardButton(text="💰Pulni kartaga yechish", callback_data="pul_yechish_karta"))
        balans.insert(InlineKeyboardButton(text="♻️Karta raqamini o'zgartirish", callback_data=f"karta_ozgartirish"))
    else:
        balans.insert(InlineKeyboardButton(text="➕Karta raqam qo'shish", callback_data=f"karta_qoshish"))
        
    balans.insert(InlineKeyboardButton(text="◀️Ortga", callback_data="ortga"))
        
    return balans

