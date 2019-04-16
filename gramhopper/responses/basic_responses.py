import abc
from telegram import Bot, Update
from telegram.message import Message


class BaseResponse(abc.ABC):
    @abc.abstractmethod
    def respond(self, bot: Bot, update: Update, response_payload: dict) -> Message:
        pass
