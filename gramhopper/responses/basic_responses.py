import abc
from telegram import Bot, Update
from telegram.message import Message
from ..representable import Representable


class BaseResponse(abc.ABC, Representable):

    @abc.abstractmethod
    def respond(self, bot: Bot, update: Update, response_payload: dict) -> Message:
        pass
