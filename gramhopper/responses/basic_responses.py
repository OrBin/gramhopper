import abc
from typing import Optional, Dict, Any

from telegram import Bot, Update
from telegram.message import Message
from ..representable import Representable


class BaseResponse(abc.ABC, Representable):
    def __init__(self, parse_mode: Optional[str] = None):
        super().__init__()
        self.__parse_mode = parse_mode

    @property
    def response_helper_kwargs(self) -> Dict[str, Any]:
        kwargs = {}

        if self.__parse_mode is not None:
            kwargs["parse_mode"] = self.__parse_mode

        return kwargs

    @abc.abstractmethod
    def respond(self, bot: Bot, update: Update, response_payload: dict) -> Message:
        pass
