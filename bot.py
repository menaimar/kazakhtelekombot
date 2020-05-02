from aiogram import Bot, Dispatcher, executor, types
from globals.functions import *
from difflib import get_close_matches
from commands import Commands

token = open_json("security/security.json")["telegram"]


bot = Bot(token=token)
dp = Dispatcher(bot)
com = Commands()


@dp.message_handler(lambda x: True)
async def main(message: types.Message):
    response = await com.exec(message)
    await message.answer(response["text"], reply_markup=create_reply_markup(None if "buttons" not in response else response["buttons"]))


@dp.callback_query_handler(lambda x: True)
async def callback(call: types.CallbackQuery):
    call.message.text = call.data
    response = await com.exec(call.message)
    await call.message.answer(response["text"], reply_markup=create_reply_markup(None if "buttons" not in response else response["buttons"]))


executor.start_polling(dp, skip_updates=True)
