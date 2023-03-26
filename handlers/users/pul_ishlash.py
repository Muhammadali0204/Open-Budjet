from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default import menu
from keyboards.inline import ovoz_berish
from loader import dp, db, bot, vaqt, taklifga_pul
from utils import get_votes
import asyncio, datetime, pytz


@dp.message_handler(text="💸Pul ishlash")
async def kfvkdnf(msg : types.Message):
    answer = f"<b>Do'stlaringizni taklif eting va har bir do'stingiz uchun <code>{taklifga_pul}</code> so'mdan pul oling 💵</b>\n\n"
    answer += f"<b>Quyidagi havolani do'stingizga yuboring, do'stingiz shu havola orqali ro'yxatdan o'tib ovoz berishi kerak.\n\nHavola 👇\n\n<code>https://t.me/openbudjet7_bot?start={msg.from_user.id}</code></b>"
    await msg.answer(answer)
    
@dp.message_handler(text="🧮Statistika")
async def lfgbklf(msg : types.Message):
    ovozlar_soni = db.select_user_by_id(5)[2]
    tolangan_summa = db.select_user_by_id(6)[2]
    foydalanuvchi_soni = db.select_users_count()[0]
    
    answer = f"<b>Botdan foydalanuvchilar soni : <code>{foydalanuvchi_soni}</code></b>\n"
    answer += f"<b>Bot orqali berilgan ovozlar soni : <code>{ovozlar_soni}</code></b>\n"
    answer += f"<b>Bot orqali to'lab berilgan summa : <code>{tolangan_summa}</code></b>"
    await msg.answer(answer)