from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default import menu
from loader import dp, db, bot, vaqt


@dp.message_handler(state=None, content_types=types.ContentTypes.ANY)
async def dkfv(msg : types.Message):
    await msg.delete()
    await msg.answer("<b>Quyidagi tugmalardan foydalaning 👇</b>", reply_markup=menu.menu)