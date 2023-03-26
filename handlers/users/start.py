from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from utils import get_votes
from keyboards.default import menu, raqam

from loader import dp, db, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    if message.text.find(" ") != -1:
        taklif_qilgan = message.text.split(" ")[1]
        if taklif_qilgan != str(message.from_user.id):
            user = db.select_user_by_id(message.from_user.id)
            if user == None:
                try:
                    db.add_user(message.from_user.id, 0, 0, None, None, None)
                except:
                    return
                await message.answer(
                    "<b>Salom, ovoz to'plashda bizga yordam bering 😊\n\n🔢Raqamingizni yuboring : </b>",
                    reply_markup=raqam.raqam,
                )
                await state.set_state("raqam")
                try :
                    db.add_taklif(message.from_user.id, taklif_qilgan)
                except : 
                    pass
            else:
                if user[3] != None:
                    await message.answer(
                        "<b>Salom, ovoz to'plashda bizga yordam bering 😊</b>",
                        reply_markup=menu.menu,
                    )
                else:
                    await message.answer(
                        "<b>🔢Raqamingizni yuboring : </b>", reply_markup=raqam.raqam
                    )
                    await state.set_state("raqam")

        else:
            user = db.select_user_by_id(message.from_user.id)
            if user[3] != None:
                await message.answer(
                    "<b>Salom, ovoz to'plashda bizga yordam bering 😊</b>",
                    reply_markup=menu.menu,
                )
            else:
                await message.answer(
                    "<b>🔢Raqamingizni yuboring : </b>", reply_markup=raqam.raqam
                )
                await state.set_state("raqam")
    else:
        user = db.select_user_by_id(message.from_user.id)
        if user == None:
            try:
                db.add_user(message.from_user.id, 0, 0, None, None, None)
            except:
                return
            await message.answer(
                "<b>Salom, ovoz to'plashda bizga yordam bering 😊\n\n🔢Raqamingizni yuboring : </b>",
                reply_markup=raqam.raqam,
            )
            await state.set_state("raqam")
        else:
            if user[3] != None:
                await message.answer(
                    "<b>Salom, ovoz to'plashda bizga yordam bering 😊</b>",
                    reply_markup=menu.menu,
                )
            else:
                await message.answer(
                    "<b>🔢Raqamingizni yuboring : </b>", reply_markup=raqam.raqam
                )
                await state.set_state("raqam")


@dp.message_handler(state="raqam", content_types=types.ContentTypes.CONTACT)
async def raqam_olish(msg: types.Message, state: FSMContext):
    raqam = msg.contact.phone_number
    if raqam.startswith("+99833") or raqam.startswith("99833"):
        await msg.answer(
            "Bu raqamingiz yaroqsiz ❌", reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state("raqam_yaroqsiz")
    elif raqam.startswith("998") and len(raqam) == 12:
        db.update_tel(f"+{raqam}", msg.from_user.id)
        await msg.answer(
            "<b>Raqamingiz muvaffaqiyatli qabul qilindi ✅\n\nMenu : </b>",
            reply_markup=menu.menu,
        )
        await state.finish()
        number = f"{raqam[3]}{raqam[4]}-{raqam[5]}{raqam[6]}{raqam[7]}-{raqam[8]}{raqam[9]}-**"
        n = 0
        data = await get_votes.get(n)
        data = data["content"]
        while data:
            for a in data:
                if a["phoneNumber"] == number:
                    db.update_ovoz(1, msg.from_user.id)
                    return

            n += 1
            data = await get_votes.get(n)
            data = data["content"]

    elif raqam.startswith("+998") and len(raqam) == 13:
        db.update_tel(raqam, msg.from_user.id)
        await msg.answer(
            "<b>Raqamingiz muvaffaqiyatli qabul qilindi ✅\n\nMenu : </b>",
            reply_markup=menu.menu,
        )
        await state.finish()
        number = f"{raqam[4]}{raqam[5]}-{raqam[6]}{raqam[7]}{raqam[8]}-{raqam[9]}{raqam[10]}-**"
        n = 0
        data = await get_votes.get(n)
        data = data["content"]
        while data:
            for a in data:
                if a["phoneNumber"] == number:
                    db.update_ovoz(1, msg.from_user.id)
                    return

            n += 1
            data = await get_votes.get(n)
            data = data["content"]
    else:
        await msg.answer(
            "Bu raqamingiz yaroqsiz ❌", reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state("raqam_yaroqsiz")


@dp.message_handler(state="raqam", content_types=types.ContentTypes.ANY)
async def raqam_yuboringda_e(msg: types.Message):
    await msg.delete()
    await msg.answer(
        "<b>🔢Iltimos, raqamingizni yuboring : </b>", reply_markup=raqam.raqam
    )


@dp.message_handler(state="raqam_yaroqsiz", content_types=types.ContentTypes.ANY)
async def djnvkdjv(msg: types.Message):
    await msg.answer("<b>Bu raqamingiz orqali botdan foydalana olmaysiz !</b>")
