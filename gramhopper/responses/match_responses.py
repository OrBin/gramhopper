from ..dict_enum import DictEnum
from telegram import Bot, Update
from .basic_responses import BaseResponse
from .response_helper import ResponseHelper


class _MatchTextResponse(BaseResponse):
    def __init__(self, template: str):
        self.template = template

    def build_response_text(self, response_payload: dict):
            return self.template.format(*response_payload['match'])


class _MatchReplyResponse(_MatchTextResponse):
    def respond(self, bot: Bot, update: Update, response_payload: dict) -> None:
        ResponseHelper.reply(bot, update, self.build_response_text(response_payload))


class _MatchMessageResponse(_MatchTextResponse):
    def respond(self, bot: Bot, update: Update, response_payload: dict) -> None:
        ResponseHelper.message(bot, update, self.build_response_text(response_payload))


class MatchResponses(DictEnum):
    reply = _MatchReplyResponse
    message = _MatchMessageResponse
