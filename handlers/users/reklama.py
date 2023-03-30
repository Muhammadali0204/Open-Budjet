from loader import db, dp, bot
from aiogram import types
from keyboards.default import menu
from aiogram.dispatcher import FSMContext
import asyncio
from data.config import ADMINS
from keyboards.inline.forward_copy import inline_key



@dp.message_handler(text=["Reklama", "reklama"], chat_id = ADMINS)
async def sendmessage(msg : types.Message, state : FSMContext):
    await msg.answer(text="<b>Reklama yuborish : </b>\n<i>(Istalgan turdagi : )</i>", reply_markup=menu.bekor)
    await msg.answer("<b>Forward yoki copy ? </b>", reply_markup=inline_key)
    await state.set_state("reklama_turi")
    
@dp.message_handler(text="❌Bekor qilish", state=['reklama_turi', 'copy', 'forward'], chat_id = ADMINS)
async def kjgjk(msg : types.Message, state : FSMContext):
    await msg.answer("❌Bekor qilindi", reply_markup=menu.menu)
    await state.finish()
    
@dp.callback_query_handler(text="for", state="reklama_turi")
async def func(call : types.CallbackQuery, state : FSMContext):
    await call.message.answer("<b>Xabarni yuboring : <i>(Forward)</i></b>")
    await state.set_state("forward")
    await call.message.delete()
    
@dp.callback_query_handler(text="copy", state="reklama_turi")
async def func(call : types.CallbackQuery, state : FSMContext):
    await call.message.answer("<b>Xabarni yuboring : <i>(Copy)</i></b>")
    await state.set_state("copy")
    await call.message.delete()
    
@dp.message_handler(state="forward", content_types=types.ContentType.ANY)
async def func(msg : types.Message, state : FSMContext):
    users = db.select_all_users()
    n = 0
    for i in range(0, len(users)):
        try:
            await bot.forward_message(users[i][0], msg.from_user.id, msg.message_id)
            n+=1
            await asyncio.sleep(0.05)
        except:
            pass
        
    await msg.answer(f"<b>{n} ta foydalanuvchiga xabar yuborildi ✅</b>\n<b>{len(users) - n} taga yuborilmadi ❌</b>", reply_markup=menu.menu)
    await state.finish()
    
@dp.message_handler(state="copy", content_types=types.ContentType.ANY)
async def func(msg : types.Message, state : FSMContext):
    users = db.select_all_users()
    n = 0
    for i in range(0, len(users)):
        try:
            await bot.copy_message(users[i][0], msg.from_user.id, msg.message_id)
            n+=1
            await asyncio.sleep(0.05)
        except:
            pass
        
    await msg.answer(f"<b>{n} ta foydalanuvchiga xabar yuborildi ✅</b>\n<b>{len(users) - n} taga yuborilmadi ❌</b>", reply_markup=menu.menu)
    await state.finish()