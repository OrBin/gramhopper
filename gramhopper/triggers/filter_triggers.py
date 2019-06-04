from functools import reduce
from typing import List, Union
from telegram import Update
from telegram.ext import Filters, BaseFilter
from ..dict_enum import DictEnum
from .trigger_result import TriggerResult
from .basic_triggers import BaseTrigger
from ..users_helper import DEFAULT_USERS_HELPER


class FilterBasedTrigger(BaseTrigger):
    """
    A base class for filter-based triggers. This is used to trigger a rule when an incoming message
    passes through the specific filter.
    """

    def __init__(self, message_filter: BaseFilter):
        """
        Constructs the trigger.

        :param message_filter: The filter to test if the message passes through
        """
        super().__init__()
        self.filter = message_filter

    def check_trigger(self, update: Update) -> TriggerResult:
        return TriggerResult(should_respond=self.filter(update.message))


class _UserFilterBasedTrigger(FilterBasedTrigger):
    """
    A user filter trigger. This is used to trigger a rule when an incoming message comes from a
    specific user.
    """

    def __init__(self, nickname: str = None, user_id: int = None, username: str = None):
        """
        Constructs the trigger.
        `nickname` can be used if such a nickname is defined in users.json file.
        Otherwise, one of `user_id` and `username` should be specified.

        :param message_filter: The filter to test if the message passes through
        :param nickname: The nickname of the user to pass messages from.
        :param user_id: The Telegram user ID of the user to pass messages from.
        :param username: The Telegram username of the user to pass messages from.
        """
        if nickname is not None:
            super().__init__(Filters.user(DEFAULT_USERS_HELPER.get_user_id_by_nickname(nickname)))
        else:
            super().__init__(Filters.user(user_id, username))


class _ChatFilterBasedTrigger(FilterBasedTrigger):
    """
    A chat filter trigger. This is used to trigger a rule when an incoming message is in a specific
    chat.
    """

    def __init__(self, chat_id: int = None, username: str = None):
        """
        Constructs the trigger.
        One and only one of `chat_id` and `username` should be specified.

        :param chat_id: The Telegram chat ID of the chat to pass messages from.
        :param username: The Telegram username whose chat to pass messages from.
        """
        super().__init__(Filters.chat(chat_id, username))


class _LanguageFilterBasedTrigger(FilterBasedTrigger):
    """
    A language filter trigger. This is used to trigger a rule when an incoming message is in a
    specific language.
    """

    def __init__(self, lang: Union[str, List[str]]):
        """
        Constructs the trigger.

        :param lang: The language code/s in which to pass messages.
        """
        super().__init__(Filters.language(lang))


class _MessageTypeFilterBasedTrigger(FilterBasedTrigger):
    """
    A message type filter trigger. This is used to trigger a rule when an incoming message is of a
    specific type.
    """

    def __init__(self, message_type):
        """
        Constructs the trigger.

        :param message_type: The message type of which to filter to pass messages, for example: \
            'photo', 'status_update.left_chat_member' or 'document'. See more in \
            :py:class:`telegram.ext.filters.Filters`.
        """
        subfilters = message_type.split('.')
        try:
            message_type_filter = reduce(getattr, subfilters, Filters)
            if isinstance(message_type_filter, BaseFilter):
                super().__init__(message_type_filter)
            else:
                raise ValueError(f'"{message_type}" is not a valid message type to filter by, '
                                 f'but it is a valid filter. Did you mean to use '
                                 f'"{message_type}" as a filter type instead?')
        except AttributeError:
            raise ValueError(f'"{message_type}" is not a valid message type to filter by.')


class FilterTriggers(DictEnum):
    """Text-based triggers."""

    user = _UserFilterBasedTrigger
    """A user filter trigger. See more in :class:`_UserFilterBasedTrigger`."""

    chat = _ChatFilterBasedTrigger
    """A user filter trigger. See more in :class:`_ChatFilterBasedTrigger`."""

    language = _LanguageFilterBasedTrigger
    """A user filter trigger. See more in :class:`_LanguageFilterBasedTrigger`."""

    message_type = _MessageTypeFilterBasedTrigger
    """A user filter trigger. See more in :class:`_MessageTypeFilterBasedTrigger`."""
