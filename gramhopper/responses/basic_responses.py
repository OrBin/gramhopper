import abc
from telegram import Bot, Update


class BaseResponse(abc.ABC):
    @abc.abstractmethod
    def respond(self, bot: Bot, update: Update, response_payload: dict) -> None:
        pass
