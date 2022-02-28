from typing import Any
from telegram import Bot, Update
from telegram.message import Message


class ResponseHelper:
    @staticmethod
    def reply(bot: Bot, update: Update, response: Any, **kwargs: Any) -> Message:
        return bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
            reply_to_message_id=update.message.message_id,
            **kwargs,
        )

    @staticmethod
    def message(bot: Bot, update: Update, response: Any, **kwargs: Any) -> Message:
        return bot.send_message(chat_id=update.effective_chat.id, text=response, **kwargs)

    @staticmethod
    def document(bot: Bot, update: Update, response: Any, **kwargs: Any) -> Message:
        return bot.send_document(chat_id=update.effective_chat.id, document=response, **kwargs)
