from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from keyboards.default import menu
from keyboards.inline import ovoz_berish
from loader import dp, db, bot, vaqt, obunachiga_pul, taklifga_pul
from utils import get_votes
from data.config import ADMINS
import asyncio, datetime, pytz


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE),text="📨Ovoz berish")
async def ovoz_berish1(msg: types.Message, state: FSMContext):
    user = db.select_user_by_id(msg.from_user.id)
    if user != None:
        try:
            time = vaqt[msg.from_user.id]
            now = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
            if now > time:
                if user[1] == 1:
                    await msg.answer(
                        "<b>Siz ovoz berib bo'lgansiz</b>\n\n<i>Ammo siz do'stlaringizni taklif qilib pul ishlashingiz mumkin.\nBatafsil : <code>💸Pul ishlash</code></i>"
                    )
                    return
                elif user[3] != None:
                    ovoz = {}
                    number = f"{user[3][4]}{user[3][5]}-{user[3][6]}{user[3][7]}{user[3][8]}-{user[3][9]}{user[3][10]}-**"
                    n = 0
                    data = await get_votes.get(n)
                    data = data["content"]
                    while data:
                        for a in data:
                            if a["phoneNumber"] == number:
                                ovoz = a
                                break

                        n += 1
                        data = await get_votes.get(n)
                        data = data["content"]

                    if ovoz == {}:
                        if user[1] == 0:
                            await msg.answer(
                                "<b>📨Ovoz berish</b>",
                                reply_markup=types.ReplyKeyboardRemove(),
                            )
                            link = db.select_user_by_id(1)[3]
                            answer = f"<b>📨<code>Ovoz berish</code> tugmasini bosing va ovoz bering\n\n<i>Ovozingiz uchun {obunachiga_pul} so'm beriladi\n\nOvoz berganingizdan so'ng, \n➕<code>Ovoz berdim</code> tugmasini bosing !</i></b>"
                            await msg.answer(
                                answer, reply_markup=ovoz_berish.ovoz_ber(link)
                            )
                            await state.set_state("ovoz ber")
                    else:
                        await msg.answer(
                            "<b>Siz ovoz berib bo'lgansiz</b>\n\n<i>Ammo siz do'stlaringizni taklif qilib pul ishlashingiz mumkin.\nBatafsil : <code>💸Pul ishlash</code></i>"
                        )
                        db.update_ovoz(1, msg.from_user.id)
                else:
                    await msg.answer(
                        "<b>Raqamingiz mavjud emas, /start ni bosing va raqamingizni yuboring </b>",
                        reply_markup=types.ReplyKeyboardRemove(),
                    )
            elif now <= time:
                t = time - now
                await msg.answer(
                    f"<b>{t.seconds//60} daqiqa {t.seconds%60} soniyadan so'ng ovoz bera olasiz!</b>"
                )
        except:
            if user[1] == 1:
                await msg.answer(
                    "<b>Siz ovoz berib bo'lgansiz</b>\n\n<i>Ammo siz do'stlaringizni taklif qilib pul ishlashingiz mumkin.\nBatafsil : <code>💸Pul ishlash</code></i>"
                )
                return
            elif user[3] != None:
                ovoz = {}
                number = f"{user[3][4]}{user[3][5]}-{user[3][6]}{user[3][7]}{user[3][8]}-{user[3][9]}{user[3][10]}-**"
                n = 0
                data = await get_votes.get(n)
                data = data["content"]
                while data:
                    for a in data:
                        if a["phoneNumber"] == number:
                            ovoz = a
                            break

                    n += 1
                    data = await get_votes.get(n)
                    data = data["content"]
                if ovoz == {}:
                    if user[1] == 0:
                        await msg.answer(
                            "<b>📨Ovoz berish</b>", reply_markup=types.ReplyKeyboardRemove()
                        )
                        link = db.select_user_by_id(1)[3]
                        answer = f"<b>📨<code>Ovoz berish</code> tugmasini bosing va ovoz bering\n\n<i>Ovozingiz uchun {obunachiga_pul} so'm beriladi\n\nOvoz berganingizdan so'ng, \n➕<code>Ovoz berdim</code> tugmasini bosing !</i></b>"
                        await msg.answer(answer, reply_markup=ovoz_berish.ovoz_ber(link))
                        await state.set_state("ovoz ber")
                else:
                    await msg.answer(
                        "<b>Siz ovoz berib bo'lgansiz</b>\n\n<i>Ammo siz do'stlaringizni taklif qilib pul ishlashingiz mumkin.\nBatafsil : <code>💸Pul ishlash</code></i>"
                    )
                    db.update_ovoz(1, msg.from_user.id)
            else:
                await msg.answer(
                    "<b>Raqamingiz mavjud emas, /start ni bosing va raqamingizni yuboring </b>",
                    reply_markup=types.ReplyKeyboardRemove(),
                )
    else:
        await msg.answer(
                    "<b>Raqamingiz mavjud emas, /start ni bosing va raqamingizni yuboring </b>",
                    reply_markup=types.ReplyKeyboardRemove(),
                )


@dp.message_handler(state="ovoz ber", content_types=types.ContentTypes.ANY)
async def hkjhjhk(msg: types.Message):
    await msg.delete()
    await msg.answer("<b>Yuqoridagi tugmalardan foydalaning !</b>")
    await asyncio.sleep(3)
    await bot.delete_message(msg.from_user.id, msg.message_id + 1)


@dp.callback_query_handler(text="ovoz_berdim", state="ovoz ber")
async def ovoz_berdi(call: types.CallbackQuery, state: FSMContext):
    # photo_id = "AgACAgIAAxkBAAPKZB285CPkrr89svWGgFGG6en88ngAAp_FMRubcPFIGi7Yt4agF5oBAAMCAAN5AAMvBA" # Meni botim uchun
    # photo_id = "AgACAgIAAxkBAAI0OGQhS5qqOKmTfC3PYaEqoqHW6NSFAALsxzEb9pkISReHZjTtZfhdAQADAgADeQADLwQ"  # Sinov bot uchun
    # photo_id = "AgACAgIAAxkBAAMJZCMUBisLbrIuWeMGBiw9fpCDDeYAAu_HMRuLaBhJQmPQoH2bu9ABAAMCAAN5AAMvBA" # Sanjarni boti uchun
    photo_id = "AgACAgIAAxkBAANYZCW2z-HC0_qV8Z5RPCzYBu3q-VIAAqvGMRsSpTBJ3qqXJuoJn5gBAAMCAAN5AAMvBA"  # Serquyosh MFY
    await call.message.delete()
    await call.message.answer_photo(
        photo=photo_id,
        caption="<b>Ovoz berganingizni tasdiqlash uchun screen shot'ni yuboring\n\n</b><i>Yuqoridagi rasmdagidek, *Ism va id'lar ko'rsatilgan holatda bo'lsin</i>",
        reply_markup=menu.bekor,
    )
    await state.set_state("rasm_yuboradi")


@dp.callback_query_handler(text="ortga", state="ovoz ber")
async def ovoz_berdi(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("<b>Menu : </b>", reply_markup=menu.menu)
    await state.finish()


@dp.message_handler(state="rasm_yuboradi", content_types=types.ContentTypes.PHOTO)
async def jnfvkj(msg: types.Message, state: FSMContext):
    await msg.answer("Bir daqiqa ...")
    ovoz = {}
    user = db.select_user_by_id(msg.from_user.id)
    if user[3] != None:
        number = f"{user[3][4]}{user[3][5]}-{user[3][6]}{user[3][7]}{user[3][8]}-{user[3][9]}{user[3][10]}-**"
        n = 0
        data = await get_votes.get(n)
        data = data["content"]
        while data:
            for a in data:
                if a["phoneNumber"] == number:
                    ovoz = a
                    break

            n += 1
            data = await get_votes.get(n)
            data = data["content"]

        await bot.delete_message(msg.from_user.id, msg.message_id + 1)
        if ovoz != {}:
            await msg.answer(
                f"<b>Ovozingiz qabul qilindi ✅\nHisobingizga {obunachiga_pul} so'm qo'shildi 💵\n\nOvoz berganingiz uchun rahmat 😊</b>\n\n<i><code>💸Pul ishlash</code> bo'limiga o'ting va pul ishlashda davom eting.</i>",
                reply_markup=menu.menu,
            )

            db.update_ovoz(1, msg.from_user.id)
            db.update_hisob(obunachiga_pul + user[2], msg.from_user.id)
            soni = db.select_user_by_id(5)[2]
            db.update_hisob(soni + 1, 5)
            taklif = db.select_taklif_qilinganmi(msg.from_user.id)
            if taklif != None and len(str(taklif[1])) >= 3:
                db.update_status(msg.from_user.id)
                taklif_qilgan_user = db.select_user_by_id(taklif[1])
                try:
                    db.update_hisob(
                        taklif_qilgan_user[2] + taklifga_pul, taklif_qilgan_user[0]
                    )
                except :
                    pass
                try:
                    await bot.send_message(
                        taklif_qilgan_user[0],
                        f"<b>Taklif qilgan do'stingiz ovoz berdi va hisobingizga <code>{taklifga_pul}</code> so'm qo'shildi\n\nHisobingiz : {taklif_qilgan_user[2] + taklifga_pul}</b>",
                    )
                except:
                    pass
            answer = f"<b>Ovoz qoshildi ✅\n\nID : <a href = 'tg://user?id={int(msg.from_user.id)}'>{msg.from_user.id}</a>\nRaqami : <code>{user[3]}</code>\n\nTopilgan natija :\n\n</b>"
            answer += f"<b>Raqam : <code>{ovoz['phoneNumber']}</code></b>\n"
            answer += f"<b>Vaqt : <code>{ovoz['voteDate']}</code></b>"
            await bot.send_photo(-1001830513983, msg.photo[-1].file_id, caption=answer)
            await state.finish()
        else:
            await msg.answer(
                "<b>Ovoz bermagansiz ❌\n\n<i>Birozdan so'ng qayta urinib ko'ring!</i></b>",
                reply_markup=menu.menu,
            )
            t = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
            t = t + datetime.timedelta(seconds=600)
            vaqt[msg.from_user.id] = t
            await state.finish()
    else:
        await msg.answer(
            "<b>Raqamingiz mavjud emas, /start ni bosing va raqamingizni yuboring </b>",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await state.finish()


@dp.message_handler(state="rasm_yuboradi", text="❌Bekor qilish")
async def sjdk(msg: types.Message, state: FSMContext):
    await msg.answer("<b>Menu : </b>", reply_markup=menu.menu)
    await state.finish()


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def mkdlfk(msg: types.Message):
    print(msg.photo[-1].file_id)
