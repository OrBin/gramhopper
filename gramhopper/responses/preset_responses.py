import abc
import random
from typing import Union, List, Optional
from telegram import Bot, Update, Document
from telegram.message import Message
from ..dict_enum import DictEnum
from .basic_responses import BaseResponse
from .response_helper import ResponseHelper


class _PresetTextResponse(BaseResponse):
    """
    A base class for preset responses. It is handling the response text building without
    handling the actual response action.
    """

    def __init__(self, preset_response: Union[str, List[str]], parse_mode: Optional[str] = None):
        """
        Constructs the response.

        :param preset_response: The preset response or list of responses
        :param parse_mode: Optional parse mode for the message. Read more in \
            :py:class:`telegram.ParseMode`.
        """
        super().__init__(parse_mode)
        self.preset_responses = preset_response

    @abc.abstractmethod
    def respond(self, bot: Bot, update: Update, response_payload: dict) -> Message:
        pass

    def get_response_text(self):
        """
        Returns the text to respond with.
        If one preset response was given, then it is returned.
        If multiple preset responses were given, one of them is randomly chosen and returned.
        :return: The text to respond with
        """
        if isinstance(self.preset_responses, str):
            return self.preset_responses
        if isinstance(self.preset_responses, list):
            return random.choice(self.preset_responses)
        return None


class _PresetDocumentResponse(BaseResponse):
    """A preset response in which the response method is a document"""

    def __init__(self, preset_response: Union[str, Document], parse_mode: Optional[str] = None):
        """
        Constructs the response.

        :param preset_response: The preset document URL or document object
        :param parse_mode: Optional parse mode for the message. Read more in \
            :py:class:`telegram.ParseMode`.
        """
        super().__init__(parse_mode)
        self.preset_response = preset_response

    def respond(self, bot: Bot, update: Update, response_payload: dict) -> Message:
        return ResponseHelper.document(
            bot,
            update,
            self.preset_response,
            **self.response_helper_kwargs,
        )


class _PresetMessageResponse(_PresetTextResponse):
    """A preset response in which the response method is a normal message"""

    def respond(self, bot: Bot, update: Update, response_payload: dict) -> Message:
        return ResponseHelper.message(
            bot,
            update,
            self.get_response_text(),
            **self.response_helper_kwargs,
        )


class _PresetReplyResponse(_PresetTextResponse):
    """A preset response in which the response method is a reply to the triggering message"""
    def respond(self, bot: Bot, update: Update, response_payload: dict) -> Message:
        return ResponseHelper.reply(
            bot,
            update,
            self.get_response_text(),
            **self.response_helper_kwargs,
        )


class PresetResponses(DictEnum):
    """
    Preset responses.
    These responses use a preset response/s to respond with. If a list of responses is given,
    one of them will be chosen randomly for each response.
    """

    document = _PresetDocumentResponse
    """A preset **document** response. See more in :class:`_PresetDocumentResponse`."""

    message = _PresetMessageResponse
    """A preset **message** response. See more in :class:`_PresetMessageResponse`."""

    reply = _PresetReplyResponse
    """A preset **reply** response. See more in :class:`_PresetReplyResponse`."""
