from aiogram import Bot, Dispatcher

from config import *

bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
