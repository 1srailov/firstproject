from aiogram.types import ReplyKeyboardMarkup

import material


langs = ReplyKeyboardMarkup(resize_keyboard=True).add('🇷🇺 RU', '🇺🇿 UZB', '🇺🇿 УЗБ')


def options_after_lang(lang: str):
    return [
            material.sections_dct[lang],
            ReplyKeyboardMarkup(resize_keyboard=True).add(
                material.ten_link_of_groups_dct[lang],
                material.groups_for_invite_dct[lang],
                material.how_to_get_dct[lang],
                material.accept_payment_dct[lang],
                material.ask_question_dct[lang],
                material.change_lang_dct[lang]
            )
    ]


