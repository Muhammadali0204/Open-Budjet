from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default import menu
from keyboards.inline import ovoz_berish, balans, bajarildi
from loader import dp, db, bot, vaqt, obunachiga_pul, karta
from utils import get_votes, is_belgi
import asyncio, datetime, pytz
from data.config import ADMINS


@dp.message_handler(text="💰Balans")
async def dfnvkjdf(msg : types.Message, state : FSMContext):
    user1 = db.select_user_by_id(msg.from_user.id)
    if user1 != None:
        answer = f"<b>💰Sizning balansingiz : <code>{user1[2]}</code> so'm</b>\n"
        answer += f"<b>📱Raqamingiz : <code>{user1[3]}</code></b>\n"
        if user1[4] != None:
            answer += f"<b>💳Kartangiz : <code>{user1[4]} ({user1[5]})</code></b>\n"
        takliflar = db.select_takliflar(msg.from_user.id)
        if takliflar == []:
            answer += "<b>🔗Taklif qilgan do'stlaringiz yo'q</b>"
        else:
            answer += f"<b>🔗Taklif qilgan do'stlaringiz soni : <code>{len(takliflar)}</code> ta</b>"
            
        answer += f"\n\n<i>Minimal {obunachiga_pul} so'm pul yecha olasiz</i>"
        await msg.answer(answer, reply_markup=balans.balans_keyboard(user1))
        await state.set_state("balans")
    else:
        await msg.answer(
                    "<b>Raqamingiz mavjud emas, /start ni bosing va raqamingizni yuboring </b>",
                    reply_markup=types.ReplyKeyboardRemove(),
                )
    
@dp.callback_query_handler(text="ortga", state = "balans")
async def kgkgf(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.message.answer("<b>Menu : </b>", reply_markup=menu.menu)
    await state.finish()
    
    
@dp.message_handler(state='balans', content_types=types.ContentTypes.ANY)
async def ansksndkj(msg : types.Message):
    await msg.delete()
    await msg.answer('<b>Yuqoridagi tugmalardan foydalaning !</b>')
    await asyncio.sleep(3)
    await bot.delete_message(msg.from_user.id, msg.message_id + 1)
    
@dp.callback_query_handler(text="pul_yechish_raqam", state= "balans")
async def sndks(call : types.CallbackQuery, state : FSMContext):
    user = db.select_user_by_id(call.from_user.id)
    if user[2] >= obunachiga_pul:
        db.update_hisob(0, call.from_user.id)
        ans = f"<b>Raqamga pul yechish : \n\nID : <code>{user[0]}</code>\nRaqam : <code>{user[3]}</code>\nMablag' : <code>{user[2]}</code></b>"
        await bot.send_message(ADMINS[0], ans, reply_markup=bajarildi.bajarildi(f"{user[0]}:{user[3]}:{user[2]}:telefon"))
        answer = f"<b><code>{user[3]}</code> raqamiga <code>{user[2]}</code> so'm mablag' tez orada tashlab beriladi 😊</b>\n\n<i>Bekor qilmoqchi bo'lsangiz @murojaat_open_budjet_bot ga, pul tashlab berilmasidan tezroq yozing.</i>"
        await call.message.answer(answer, reply_markup=menu.menu)
    else:
        await call.answer("Yechib olish uchun maglag' yetarli emas ❌", show_alert=True)
        await call.message.answer("<b>Menu : </b>", reply_markup=menu.menu)
    await call.message.delete()
    await state.finish()
    
    
@dp.callback_query_handler(text="pul_yechish_boshqa_raqam", state= "balans")
async def sndks(call : types.CallbackQuery, state : FSMContext):
    user = db.select_user_by_id(call.from_user.id)
    if user[2] >= obunachiga_pul:
        await call.message.answer("<b>Telefon raqamini yuboring : \n\n</b><i>Namuna : +998901234567</i>", reply_markup=menu.bekor)
        await state.set_state("tel_raqam_yuborish")
    else:
        await call.answer("Yechib olish uchun maglag' yetarli emas ❌", show_alert=True)
        await call.message.answer("<b>Menu : </b>", reply_markup=menu.menu)
        await state.finish()
        
    await call.message.delete()
        

@dp.message_handler(text="❌Bekor qilish", state=["tel_raqam_yuborish", 'karta_raqam_yuborish', "karta_egasi_ismi", "search"])
async def sfgklfmbgk(msg : types.Message, state : FSMContext):
    await msg.answer('<b>❌Bekor qilindi\n\nMenu : </b>', reply_markup=menu.menu)
    await state.finish()
    
@dp.message_handler(state="tel_raqam_yuborish", content_types=types.ContentTypes.ANY)
async def skjosdvnnosv(msg : types.Message, state : FSMContext):
    raqam = msg.text
    if raqam.startswith(('+99890', '+99891', '+99893', '+99894', '+99895', '+99897', '+99899', '+99888')) and len(raqam) == 13 and raqam[1:13].isnumeric():
        user = db.select_user_by_id(msg.from_user.id)
        db.update_hisob(0, msg.from_user.id)
        ans = f"<b>Raqamga pul yechish : \n\nID : <code>{user[0]}</code>\nRaqam : <code>{raqam}</code>\nMablag' : <code>{user[2]}</code></b>"
        await bot.send_message(ADMINS[0], ans, reply_markup=bajarildi.bajarildi(f"{user[0]}:{raqam}:{user[2]}:telefon"))
        answer = f"<b><code>{raqam}</code> raqamiga <code>{user[2]}</code> so'm mablag' tez orada tashlab beriladi 😊</b>\n\n<i>Bekor qilmoqchi bo'lsangiz @murojaat_open_budjet_bot ga, pul tashlab berilmasidan tezroq yozing.</i>"
        await msg.answer(answer, reply_markup=menu.menu)
        await state.finish()
    else:
        await msg.answer("<b>Bu raqam yaroqsiz ❌, boshqa raqam yuboring : </b>", reply_markup=menu.bekor)
        
@dp.callback_query_handler(text="pul_yechish_karta", state= "balans")
async def sndks(call : types.CallbackQuery, state : FSMContext):
    user = db.select_user_by_id(call.from_user.id)
    if user[2] >= obunachiga_pul:
        db.update_hisob(0, call.from_user.id)
        ans = f"<b>Kartaga pul yechish : \nID : <code>{user[0]}</code>\nKarta raqam : <code>{user[4]}({user[5]})</code>\nMablag' : <code>{user[2]}</code></b>"
        await bot.send_message(ADMINS[0], ans, reply_markup=bajarildi.bajarildi(f"{user[0]}:{user[3]}:{user[2]}:karta"))
        answer = f"<b><code>{user[4]}</code> karta raqamiga <code>{user[2]}</code> so'm mablag' tez orada o'tkazib beriladi 😊</b>\n\n<i>Bekor qilmoqchi bo'lsangiz @murojaat_open_budjet_bot ga, pul tashlab berilmasidan tezroq yozing.</i>"
        await call.message.answer(answer, reply_markup=menu.menu)
    else:
        await call.answer("Yechib olish uchun maglag' yetarli emas ❌", show_alert=True)
        await call.message.answer("<b>Menu : </b>", reply_markup=menu.menu)
    await call.message.delete()
    await state.finish()
    

@dp.callback_query_handler(text=["karta_qoshish", 'karta_ozgartirish'], state= "balans")
async def sndks1(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.message.answer("<b>Karta raqam yuboring : </b>\n\n<i>Faqat Humo yoki Uzcard (8600..., 9860...)\nNamuna : 8600123412341234 (16 ta)</i>", reply_markup=menu.bekor)
    await state.set_state("karta_raqam_yuborish")
    
@dp.message_handler(state= "karta_raqam_yuborish")
async def sndks(msg : types.Message, state : FSMContext):
    karta1 = msg.text
    if karta1.isnumeric() and karta1.startswith(('8600', '9860')) and len(karta1) == 16:
        await msg.answer(f"<b><code>{karta1}</code> ushbu karta kimga tegishli ekanini yuboring : </b>\n<i>Ism familiya to'liq yuborilishi shart emas, misol uchun : \n<code>Anvar M.</code></i>", reply_markup=menu.bekor)
        karta[msg.from_user.id] = karta1
        await state.set_state('karta_egasi_ismi')
    else:
        await msg.answer("<b>Yaroqsiz karta raqami ❌</b>\n<i>Boshqa raqam yuboring : </i>", reply_markup=menu.bekor)
        
        
@dp.message_handler(state="karta_egasi_ismi")
async def sdkclamka(msg : types.Message, state : FSMContext):
    egasi = msg.text
    if all(x.isalpha() or is_belgi.nuqta_space(x) for x in egasi):
        db.update_karta(karta[msg.from_user.id], msg.from_user.id)
        db.update_karta_egasi(egasi, msg.from_user.id)
        await msg.answer("<b>Kartangiz qabul qilindi ✅</b>", reply_markup=menu.menu)
        await state.finish()
    else:
        await msg.answer("<b>Bu ism yaroqsiz ❌, faqat lotin harflari, nuqta va bo'sh joy ishlata olasiz!</b>\n\n<i>Qayta yuboring : </i>", reply_markup=menu.bekor)
        