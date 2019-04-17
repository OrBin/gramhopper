import abc
from telegram import Bot, Update
from telegram.message import Message
from ..dict_enum import DictEnum
from .basic_responses import BaseResponse
from .response_helper import ResponseHelper


class _MatchTextResponse(BaseResponse):
    """
    A base class for regexp-based responses. It is handling the response text building without
    handling the actual response action.
    """

    def __init__(self, template: str):
        """
        Constructs the response.

        :param template: The template to use when building the response text
        """
        super().__init__()
        self.template = template

    @abc.abstractmethod
    def respond(self, bot: Bot, update: Update, response_payload: dict) -> Message:
        pass

    def build_response_text(self, response_payload: dict):
        return self.template.format(*response_payload['match'])


class _MatchMessageResponse(_MatchTextResponse):
    """A regexp-based response in which the response method is a normal message"""

    def respond(self, bot: Bot, update: Update, response_payload: dict) -> Message:
        return ResponseHelper.message(bot, update, self.build_response_text(response_payload))


class _MatchReplyResponse(_MatchTextResponse):
    """A regexp-based response in which the response method is a reply to the triggering message"""

    def respond(self, bot: Bot, update: Update, response_payload: dict) -> Message:
        return ResponseHelper.reply(bot, update, self.build_response_text(response_payload))


class MatchResponses(DictEnum):
    """
    Regexp-based responses.
    These responses use the regexp match result from the trigger, as well as the given template,
    to build the response text.
    """

    message = _MatchMessageResponse
    """A regexp-based **message** response. See more in :class:`_MatchMessageResponse`."""

    reply = _MatchReplyResponse
    """A regexp-based **reply** response. See more in :class:`_MatchReplyResponse`."""
