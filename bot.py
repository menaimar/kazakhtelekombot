from aiogram import Bot, Dispatcher, executor, types
from globals.functions import *
from difflib import get_close_matches

token = open_json("security/security.json")["main"]
tree = open_json("main_tree.json")

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(func=lambda x: True)
async def main():
    pass


executor.start_polling(dp, skip_updates=True)
