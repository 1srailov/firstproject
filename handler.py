from email.mime import image
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import executor

import material
from bot import *

import keyboard

from databse import *
dt = Database()
# Need to change to database!
user_lang = '🇷🇺 RU'
waiting_for_question = False
image_accept = False

@dp.message_handler(commands=["start"])
async def language(msg: Message):
    if(msg.from_user.id == admin_id):
      await msg.answer("welcome admin!")

    text = "Выберите язык / Tilni tanlang / Тилни танланг:"
    await msg.answer(text, reply_markup=keyboard.langs)


@dp.message_handler()
async def menus(msg: Message):
    if(msg.from_user.id == admin_id):
        lst = msg.text.split("_")
        await bot.send_message(int(lst[0]), lst[1])



    # Here need to declare database object
    global user_lang
    global waiting_for_question
    global image_accept

    if msg.text in ['🇷🇺 RU', '🇺🇿 UZB', '🇺🇿 УЗБ']:
        res = keyboard.options_after_lang(msg.text)

        # Need to save it to database
        user_lang = msg.text

       

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

    #chek_payment
    elif msg.text in list(material.accept_payment_dct.values()):
        text = material.check_payment[user_lang]
        await msg.answer(text)
        image_accept = True

    # Changing language
    elif msg.text in list(material.change_lang_dct.values()):
        text = "Выберите язык / Tilni tanlang / Тилни танланг:"

        await msg.answer(text, reply_markup=keyboard.langs)

    # User asking Question
    elif msg.text in list(material.ask_question_dct.values()):
        text = material.reply_for_question.get(user_lang)

        await msg.answer(text, reply_markup=ReplyKeyboardRemove())
        
        # Need to Update it from Database
        waiting_for_question = True
    else:
        if waiting_for_question:
            await bot.send_message(admin_id,f"user_id = {msg.from_user.id}\nquestion = {msg.text}")
            # Need to update from Database                      
            waiting_for_question = False
        print("This is ask option")

        


@dp.message_handler(content_types=['photo'])
async def accepting(msg:Message):
    global image_accept
    if image_accept:
            await bot.send_photo(admin_id,msg.photo[len(msg.photo) - 1].file_id)
            await bot.send_message(admin_id, msg.from_user.id)
            image_accept = False







if __name__ == "__main__":
    print("Started")

    executor.start_polling(dp)
