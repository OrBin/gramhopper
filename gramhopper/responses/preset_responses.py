import random
from ..dict_enum import DictEnum
from typing import Union, List
from telegram import Bot, Update, Document
from .basic_responses import BaseResponse
from .response_helper import ResponseHelper


class _PresetTextResponse(BaseResponse):
    def __init__(self, preset_response: Union[str, List[str]]):
        self.preset_responses = preset_response

    def get_response_text(self):
        if isinstance(self.preset_responses, str):
            return self.preset_responses
        elif isinstance(self.preset_responses, list):
            return random.choice(self.preset_responses)


class _PresetReplyResponse(_PresetTextResponse):
    def respond(self, bot: Bot, update: Update, response_payload: dict) -> None:
        ResponseHelper.reply(bot, update, self.get_response_text())


class _PresetMessageResponse(_PresetTextResponse):
    def respond(self, bot: Bot, update: Update, response_payload: dict) -> None:
        ResponseHelper.message(bot, update, self.get_response_text())


class _PresetDocumentResponse(BaseResponse):
    def __init__(self, preset_response: Union[str, Document]):
        self.preset_response = preset_response

    def respond(self, bot: Bot, update: Update, response_payload: dict) -> None:
        ResponseHelper.document(bot, update, self.preset_response)


class PresetResponses(DictEnum):
    reply = _PresetReplyResponse
    message = _PresetMessageResponse
    document = _PresetDocumentResponse
