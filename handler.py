from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import executor

import material
import keyboard

from database.database import Database
from bot import *


user_referal = 'https://telegram.me/{}?start={}'

db = Database()


@dp.message_handler(commands=["start"])
async def language(msg: Message):
    user_id = msg.from_user.id

    if user_id == admin_id:
        await msg.answer("Welcome admin!")
        return

    splitted = msg.text.split()

    # it will check if user exist
    if not await db.user_exists(user_id):
        await db.add_user(user_id)
        if len(splitted) == 2:
            await db.increase_ref_count(splitted[1])

    text = "Выберите язык / Tilni tanlang / Тилни танланг:"
    await msg.answer(text, reply_markup=keyboard.langs)


@dp.message_handler()
async def menus(msg: Message):
    user_id = msg.from_user.id

    if user_id == admin_id:
        lst = msg.text.split("_")
        await bot.send_message(int(lst[0]), lst[1])

        return

    # For Users
    user_lang = await db.get_user_lang(user_id)

    if msg.text in ['🇷🇺 RU', '🇺🇿 UZB', '🇺🇿 УЗБ']:
        res = keyboard.options_after_lang(msg.text)

        await db.update_user_lang(msg.text, user_id)

        await msg.answer(
            res[0],  # Text
            reply_markup=res[1]  # KeyboardMarkup
        )

    # 10 ссылок групп
    elif msg.text in list(material.ten_link_of_groups_dct.values()):
        await msg.answer(
            material.text_for_introduction_dct[user_lang]  # Вот ссылка на некоторые из них для ознакомления :
            + material.ten_sample_links_str  # https://t.me/....
        )

    # check_payment
    elif msg.text in list(material.accept_payment_dct.values()):
        text = material.check_payment[user_lang]
        await msg.answer(text)

        await db.update_image_accept(True, user_id)

    # Changing language
    elif msg.text in list(material.change_lang_dct.values()):
        text = "Выберите язык / Tilni tanlang / Тилни танланг:"

        await msg.answer(text, reply_markup=keyboard.langs)

        await db.update_user_lang(msg.text, user_id)

    # How get
    elif msg.text in list(material.how_to_get_dct.values()):
        text = material.how_get[user_lang]
        await msg.answer(text)

    # Referal
    elif msg.text in list(material.groups_for_invite_dct.values()):

        text = material.answer_for_referal[user_lang]
        await msg.answer(text)

        text = user_referal.format('sng_logistic_bot', user_id)
        await msg.reply(text)

        count = await db.get_ref_count(user_id)
        await msg.reply(text=f'Count: {count}')

    # User asking Question
    elif msg.text in list(material.ask_question_dct.values()):
        text = material.reply_for_question.get(user_lang)

        await msg.answer(text, reply_markup=ReplyKeyboardRemove())

        await db.update_wait_question(True, user_id)

    # Other conditions
    else:
        if db.get_user_waiting_question(user_id):
            await bot.send_message(admin_id, f"user_id = {user_id}\nquestion = {msg.text}")

            await db.update_wait_question(False, user_id)

            await msg.answer(material.answer_for_question[user_lang],
                             reply_markup=keyboard.options_after_lang(user_lang)[1])

        print("This is ask option")


@dp.message_handler(content_types=['photo'])
async def accepting(msg: Message):
    user_id = msg.from_user.id

    image_accept = await db.get_image_accept(user_id)

    if image_accept:
        await bot.send_photo(admin_id, msg.photo[len(msg.photo) - 1].file_id)
        await bot.send_message(admin_id, user_id)

        await db.update_image_accept(False, user_id)


if __name__ == "__main__":
    print("Started")

    executor.start_polling(dp)
