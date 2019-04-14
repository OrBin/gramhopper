from typing import Any
from telegram import Bot, Update
from telegram.message import Message


class ResponseHelper:
    @staticmethod
    def reply(bot: Bot, update: Update, response: Any) -> Message:
        return bot.send_message(chat_id=update.effective_chat.id,
                                text=response,
                                reply_to_message_id=update.message.message_id)

    @staticmethod
    def message(bot: Bot, update: Update, response: Any) -> Message:
        return bot.send_message(chat_id=update.effective_chat.id, text=response)

    @staticmethod
    def document(bot: Bot, update: Update, response: Any) -> Message:
        return bot.send_document(update.effective_chat.id, response)
