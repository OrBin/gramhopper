import re
from typing import List, Union
from telegram import Update
from .trigger_result import TriggerResult
from ..dict_enum import DictEnum
from .basic_triggers import BaseTrigger


class _RegExpTrigger(BaseTrigger):
    """
    Regular-expression-based trigger. This is used to trigger a rule when an incoming message
    matches the given pattern.
    """

    def __init__(self, pattern: str):
        """
        Constructs the trigger.

        :param pattern: The pattern to test the message's match with
        """
        super().__init__()
        self.pattern = pattern

    def check_trigger(self, update: Update) -> TriggerResult:
        if update.message.text is not None:
            text = update.message.text.replace('\n', ' ')
            match = re.match(self.pattern, text)
            if match is not None:
                return TriggerResult(should_respond=True,
                                     response_payload={'match': match.groups()})

        return TriggerResult(should_respond=False)


class _HasSubstringTrigger(_RegExpTrigger):
    """
    Substring trigger. This is used to trigger a rule when a certain substring  (or one of a list
    of substrings) exists in an incoming message.
    """

    def __init__(self, substring: Union[str, List[str]], exact: bool = False):
        """
        Constructs the trigger.

        :param substring: The substring/s to search in the message
        :param exact: Whether the exact substring should appear (as a whole word) in the message
        """
        if isinstance(substring, str):
            regexp_for_substring = substring
        elif isinstance(substring, list):
            if self.validate_strings_list(substring):
                regexp_for_substring = '|'.join(substring)
            else:
                raise TypeError('Parameter \'substring\' should be either a string or a list of '
                                'strings, but a list containing non-strings was given.')
        else:
            raise TypeError(f'Parameter \'substring\' should be either a string or a list of '
                            f'strings, but {type(substring)} was given')

        prefix = '(?:.* )?' if exact else '.*'
        postfix = '(?: .*)?' if exact else '.*'
        super().__init__(f'^{prefix}({regexp_for_substring}){postfix}$')

    @staticmethod
    def validate_strings_list(strings):
        return all(map(lambda element: isinstance(element, str), strings))


class _HasExactWordTrigger(_HasSubstringTrigger):
    """
    Word trigger - the same as substring trigger, but for exact words search. This is used to
    trigger a rule when a certain word (or one of a list of words) exists in an incoming message.
    """

    def __init__(self, word: Union[str, List[str]]):
        """
        Constructs the trigger.

        :param word: The word/s to search in the message
        """
        try:
            super().__init__(word, exact=True)
        except TypeError:
            raise TypeError(f'Parameter \'word\' should be either a string or a list of strings '
                            f'({type(word)} given)')


class TextTriggers(DictEnum):
    """Text-based triggers."""

    has_substring = _HasSubstringTrigger
    """A substring trigger. See more in :class:`_HasSubstringTrigger`."""

    has_exact_word = _HasExactWordTrigger
    """A word trigger. See more in :class:`_HasExactWordTrigger`."""

    regexp = _RegExpTrigger
    """A regexp-based trigger. See more in :class:`_RegExpTrigger`."""
