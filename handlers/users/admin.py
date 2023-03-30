from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from keyboards.default import menu
from utils import get_votes
from keyboards.inline import ovoz_berish
from loader import dp, db, bot, tolangan_malumot, obunachiga_pul, taklifga_pul
from data.config import ADMINS
import asyncio, datetime, pytz


@dp.callback_query_handler(regexp="bajarildi:+")
async def kjljfb(call : types.CallbackQuery, state : FSMContext):
    msga =  call.message.html_text
    
    msga += "\n\n<b>To'lab berildi ✅</b>"
    
    await call.message.edit_text(msga)
    
    data = call.data
    
    tolangan_malumot[1] = data.split(':')
    
    

    await bot.send_message(ADMINS[0],"<b>Screen shot ni yuboring : \n\nRasm foydalanuvchiga yuboriladi</b>")
    
    
    
@dp.message_handler(content_types=types.ContentTypes.PHOTO, chat_id = ADMINS)
async def djjkdv(msg : types.Message, state : FSMContext):
    try :
        malumot = tolangan_malumot[1]
    except :
        return
    if malumot != None:
        answer = f"<b><code>{malumot[2]}</code> {malumot[4]} raqamiga <code>{malumot[3]}</code> so'm mablag' o'tkazildi ✅</b>"
        try:
            await bot.send_photo(chat_id = malumot[1],photo= msg.photo[-1].file_id, caption=answer)
            await msg.answer(f"<b>Yetkazildi ✅\n\nID : <a href = 'tg://user?id={malumot[1]}'>{malumot[1]}</a></b>")
        except :
            await msg.answer(f"<b>Rasm yuborilmadi ❌\n\nID : <a href = 'tg://user?id={malumot[1]}'>{malumot[1]}</a></b>")
            
        await bot.send_photo(-1001931751704, photo=msg.photo[-1].file_id, caption=answer)
        hisob = db.select_user_by_id(6)[2]
        db.update_hisob(hisob + int(malumot[3]),6)
        tolangan_malumot[1] = None
    

    
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE),regexp="Ovoz pul:+", chat_id = ADMINS)
async def mkdfkv(msg : types.Message):
    pul = msg.text.split(':')[1]
    if pul.isnumeric():
        db.update_hisob(pul, 3)
        await msg.answer(f"{pul} ga o'zgardi")
    else:
        await msg.answer("O'zgarmadi")
        
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE),regexp="Ovoz link~+", chat_id = ADMINS)
async def mkdfkv(msg : types.Message):
        db.update_tel(msg.text.split("~")[1], 1)
        await msg.answer(f"{msg.text} ga o'zgardi")
        
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE),regexp="Baza~+", chat_id = ADMINS)
async def mkdfkv(msg : types.Message):
        db.update_tel(msg.text.split("~")[1], 2)
        await msg.answer(f"{msg.text} ga o'zgardi")
        
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE),regexp="Taklif pul:+", chat_id = ADMINS)
async def mkdfkv(msg : types.Message):
    pul = msg.text.split(':')[1]
    if pul.isnumeric():
        db.update_hisob(pul, 4)
        await msg.answer(f"{pul} ga o'zgardi")
    else:
        await msg.answer("O'zgarmadi")
        
@dp.message_handler(text='/get', chat_id = ADMINS)
async def kfnk(msg : types.Message):
    ovoz_link = db.select_user_by_id(1)[3]
    Baza = db.select_user_by_id(2)[3]

    
    await msg.answer(f"<b>Ovoz link : <code>{ovoz_link}</code>\nBaza : <code>{Baza}</code>\nOvoz narxi : {obunachiga_pul}\nTaklif narxi : {taklifga_pul}</b>\n\nLink  va narxlarni o'zgartirish : (+ ni o'rniga narx yoki link yoziladi)\n\nOvoz pul:+\nTaklif pul:+\nOvoz link~+\nBaza~+")
    
    
    
    
    
    
    
    
@dp.message_handler(text="/search", chat_id = ADMINS)
async def kdnv(msg : types.Message, state : FSMContext):
    await msg.answer("Raqam yuboring : \n\n901234567 ko'rinishida", reply_markup=menu.bekor)
    await state.set_state("search")
    
    
@dp.message_handler(state="search")
async def ksjdvjb(msg : types.Message, state : FSMContext):
    raqam = msg.text
    if raqam.isnumeric() and len(raqam) == 9:
        ovoz = []
        number = f"{raqam[0]}{raqam[1]}-{raqam[2]}{raqam[3]}{raqam[4]}-{raqam[5]}{raqam[6]}-**"
        n = 0
        data = await get_votes.get(n)
        data = data["content"]
        while data:
            for a in data:
                if a["phoneNumber"] == number:
                    ovoz.append(a)

            n += 1
            data = await get_votes.get(n)
            data = data["content"]
        if ovoz != []:
            ans = "<b>Natijalar : \n\n</b>"
            for o in ovoz:
                ans += f"<b>Raqam : {o['phoneNumber']}\nVaqt : {o['voteDate']}</b>\n\n"
            
            await msg.reply(ans, reply_markup=menu.menu)
            await state.finish()
                
            
        else:
            await msg.reply("Topilmadi", reply_markup=menu.menu)
            await state.finish()
            
            
    else:
        await msg.answer("Xato, booshqatdan yoki bekor qiling", reply_markup=menu.bekor)