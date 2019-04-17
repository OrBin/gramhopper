import abc
from telegram import Bot, Update
from telegram.message import Message


class BaseResponse(abc.ABC):
    @abc.abstractmethod
    def respond(self, bot: Bot, update: Update, response_payload: dict) -> Message:
        pass

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def __str__(self):
        try:
            return self.__name
        except AttributeError:
            return f'inline {self.__class__.__name__}'
