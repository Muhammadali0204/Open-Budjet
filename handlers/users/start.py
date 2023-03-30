from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from utils import get_votes
from keyboards.default import menu, raqam

from loader import dp, db, bot, taklifga_pul


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE),CommandStart())
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
                    f"<b>Salom {message.from_user.get_mention(message.from_user.full_name)}, ovoz to'plashda bizga yordam bering 😊\n\n🔢Raqamingizni yuboring : </b>",
                    reply_markup=raqam.raqam,
                )
                await state.set_state("raqam")
                try :
                    db.add_taklif(message.from_user.id, taklif_qilgan)
                except : 
                    pass
                try :
                    await bot.send_message(taklif_qilgan, f"<b>Siz taklif qilgan <a href = 'tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a> /start bosdi\nHisobingizga {taklifga_pul} so'm mablag' qo'shilishi uchun taklif qilgan odamingiz ovoz berishi kerak !</b>")
                except :
                    pass
            else:
                if user[3] != None:
                    await message.answer(
                        f"<b>Salom {message.from_user.get_mention(message.from_user.full_name)}, ovoz to'plashda bizga yordam bering 😊</b>",
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
                    f"<b>Salom {message.from_user.get_mention(message.from_user.full_name)}, ovoz to'plashda bizga yordam bering 😊</b>",
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
                f"<b>Salom {message.from_user.get_mention(message.from_user.full_name)}, ovoz to'plashda bizga yordam bering 😊\n\n🔢Raqamingizni yuboring : </b>",
                reply_markup=raqam.raqam,
            )
            await state.set_state("raqam")
        else:
            if user[3] != None:
                await message.answer(
                    f"<b>Salom {message.from_user.get_mention(message.from_user.full_name)}, ovoz to'plashda bizga yordam bering 😊</b>",
                    reply_markup=menu.menu,
                )
            else:
                await message.answer(
                    "<b>🔢Raqamingizni yuboring : </b>", reply_markup=raqam.raqam
                )
                await state.set_state("raqam")


@dp.message_handler(state="raqam", content_types=types.ContentTypes.CONTACT)
async def raqam_olish(msg: types.Message, state: FSMContext):
    raqam1 = msg.contact.phone_number
    user_id = msg.contact.user_id
    if user_id == msg.from_user.id:
        if raqam1.startswith("+99833") or raqam1.startswith("99833"):
            await msg.answer(
                "Ovoz berish jarayonida Humans raqamidan foydalanishga ruxsat etilmaydi ❌", reply_markup=types.ReplyKeyboardRemove()
            )
            await state.set_state("raqam_yaroqsiz")
        elif raqam1.startswith("998") and len(raqam1) == 12:
            db.update_tel(f"+{raqam1}", msg.from_user.id)
            await msg.answer(
                "<b>Raqamingiz muvaffaqiyatli qabul qilindi ✅</b>",
                reply_markup=menu.menu,
            )
            await state.finish()
            number = f"{raqam1[3]}{raqam1[4]}-{raqam1[5]}{raqam1[6]}{raqam1[7]}-{raqam1[8]}{raqam1[9]}-**"
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

        elif raqam1.startswith("+998") and len(raqam1) == 13:
            db.update_tel(raqam1, msg.from_user.id)
            await msg.answer(
                "<b>Raqamingiz muvaffaqiyatli qabul qilindi ✅</b>",
                reply_markup=menu.menu,
            )
            await state.finish()
            number = f"{raqam1[4]}{raqam1[5]}-{raqam1[6]}{raqam1[7]}{raqam1[8]}-{raqam1[9]}{raqam1[10]}-**"
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
                "Chet el nomerlaridan ovoz berishga ruxsat etilmaydi ❌", reply_markup=types.ReplyKeyboardRemove()
            )
            await state.set_state("raqam_yaroqsiz")
    else:
        await msg.answer("<b>Bu sizning raqamingiz emas ❌\n\nO'zingizni raqamingizni quyidagi tugma orqali yuboring : </b>", reply_markup=raqam.raqam)


@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE),state="raqam", content_types=types.ContentTypes.ANY)
async def raqam_yuboringda_e(msg: types.Message):
    await msg.delete()
    await msg.answer(
        "<b>🔢Iltimos, raqamingizni yuboring : </b>", reply_markup=raqam.raqam
    )


@dp.message_handler(state="raqam_yaroqsiz", content_types=types.ContentTypes.ANY)
async def djnvkdjv(msg: types.Message):
    await msg.answer("<b>Bu raqamingiz orqali botdan foydalana olmaysiz !</b>")
    
    
@dp.message_handler(filters.ChatTypeFilter(types.ChatType.PRIVATE),text="📝Yoriqnoma")
async def dlfvkj(msg : types.Message):
    answer = "<b>1. <code>📨Ovoz berish</code> tugmasini bosing.\n2. Botdan kelgan xabar ostidagi <code>📨Ovoz berish</code> tugmasini bosing.\n3. Tugmasini bosish orqali Open budjetning rasmiy botiga o'tasiz.\n4. start'ni bosing, kelgan xabar ostidagi tugmalarni <code>Ovoz berish</code> tugmasini bosing.\n5. So'ngra <code>Ha, tasdiqlayman</code> tugmasini.\n6. Ovozingiz qabul qilingandan so'ng, o'sha yerning o'zida screen shot qiling.\n7. Bu botga qayting va <code>➕Ovoz berdim</code> tugmasini bosing.\n8. Screen shotni yuboring va pullaringizni oling 💰</b>"
    await msg.answer(answer)
