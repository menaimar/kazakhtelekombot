from aiogram import Bot


class Commands:
    def __init__(self, bot: Bot):
        self.cache = {}
        self.bot = bot

    def exec(self, name: str, **kwargs):
        attr = self.__getattribute__(name)
        if "chat_id" in kwargs:
            chat_id = kwargs["chat_id"]
            if chat_id not in self.cache:
                self.cache[chat_id] = {
                    "state": "start"
                }
        if callable(attr):
            return attr(**kwargs)

    def start(self, chat_id=None):
        self.bot.send_message(chat_id, "")


