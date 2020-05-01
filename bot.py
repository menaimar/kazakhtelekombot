from aiogram import Bot, Dispatcher, executor, types
from globals.functions import *
from difflib import get_close_matches
from commands import Commands

token = open_json("security/security.json")["main"]


bot = Bot(token=token)
dp = Dispatcher(bot)
com = Commands()


@dp.message_handler(func=lambda x: True)
async def main(message: types.Message):
    response = await com.exec(message)
    await message.reply(response["text"], create_reply_markup(None if "buttons" not in response else response["buttons"]))


executor.start_polling(dp, skip_updates=True)
