from aiogram import Bot, types
from globals.functions import *
from globals.globals import *


class Commands:
    def __init__(self):
        self.cache = {}
        self.tree = open_json("main_tree.json")
        self.text = open_json("main_text.json")
        self.uncommon_text = open_json("uncommon_text.json")

    async def exec(self, message: types.Message):
        chat_id = message.chat.id
        if chat_id not in self.cache:
            self.cache[chat_id] = {
                "state": "start",
                "lang": "ru",
                "address": {}
            }

        command = message.get_command()
        if command in langs:
            self.cache[chat_id]["lang"] = command
        current_state, lang = self.cache[chat_id]["state"], self.cache[chat_id]["lang"]
        default_response = ""
        response_function = ""
        if current_state in self.text[lang]:
            default_response = self.text["start"] if current_state == "start" else self.text[lang][current_state]
            response_function = await self.default(message)
        else:
            response_function = await self.__getattribute__(current_state)(message)
        return response_function if response_function else default_response

    async def default(self, message: types.Message = None):
        chat_id = message.chat.id
        current_state = self.cache[chat_id]["state"]
        text = message.text
        ints = []
        if current_state in addresses:
            if current_state in ints:
                if is_int(text):
                    self.cache[chat_id]["address"][current_state] = text
                    self.next_state(chat_id)
                    return
                else:
                    return {"text": "Оно должно быть числом"}
        else:
            self.cache[chat_id]["address"][current_state] = text
        self.next_state(chat_id)

    def next_state(self, chat_id):
        current_state = self.cache[chat_id]["state"]
        self.cache[chat_id]["state"] = self.tree[current_state][0]

    # Необычные респонсы
    async def check_availability(self, message: types.Message = None):
        chat_id = message.chat.id
        current_state = self.cache[chat_id]["state"]
        ktreq = self.cache[chat_id]["address"]
        await message.reply("Проверяем адресс...")
        check = ktcheck(ktreq)
        if check:
            response = "Ваш адрес доступен к подключению"
        else:
            response = "Увы.."
        self.cache[chat_id]["state"] = self.tree[current_state][check]
        return {"text": response}

    async def asking(self, message: types.Message = None):
        chat_id = message.chat.id
        current_state = self.cache[chat_id]["state"]
        check = message.text == "Купить"
        if check:
            buy()
        self.cache[chat_id]["state"] = self.tree[current_state][check]
    # ------------------------

    def check_strs(self, text, chat_id):
        current_state = self.cache[chat_id]
        section_list = self.get_section_list(chat_id)
        name_list = list(map(lambda x: x['name'], section_list))
        if text in name_list:
            index = name_list.index(text)
            self.cache[chat_id]["address"][current_state] = section_list[index]["id"]
        else:
            get_close_matches(text, name_list)

    def get_section_list(self, chat_id):
        current_state = self.cache[chat_id]
        address = self.cache[chat_id]["address"]
        if current_state == "region":
            return list(map(lambda x: {"id": regions[x], "name": x}, regions))
        elif current_state == "city":
            return get_cities(address["region"])
        elif current_state == "street":
            return get_streets(address["region"], address["city"])
