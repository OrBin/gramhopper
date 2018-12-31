from typing import Any
from telegram import Bot, Update


class ResponseHelper:
    @staticmethod
    def reply(bot: Bot, update: Update, response: Any):
        update.message.reply_text(response)


    @staticmethod
    def message(bot: Bot, update: Update, response: Any):
        bot.send_message(chat_id=update.effective_chat.id, text=response)


    @staticmethod
    def document(bot: Bot, update: Update, response: Any):
        bot.send_document(update.effective_chat.id, response)
