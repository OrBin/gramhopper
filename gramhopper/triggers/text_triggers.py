import re
from ..dict_enum import DictEnum
from typing import List, Union
from telegram import Update
from .basic_triggers import BaseTrigger
from ..trigger_result import TriggerResult

class _RegExpTrigger(BaseTrigger):
    def __init__(self, pattern: str):
        self.pattern = pattern

    def check_trigger(self, update: Update) -> TriggerResult:
        if update.message.text is not None:
            text = update.message.text.replace('\n', ' ')
            match = re.match(self.pattern, text)
            if match is not None:
                return TriggerResult(should_respond=True,
                                     response_payload={ 'match': match.groups() })

        return TriggerResult(should_respond=False)


class _HasSubstringTrigger(_RegExpTrigger):
    def __init__(self, substring: Union[str, List[str]], exact: bool = False):
        if isinstance(substring, str):
            regexp_for_substring = substring
        elif isinstance(substring, list):
            if self.validate_strings_list(substring):
                regexp_for_substring = '|'.join(substring)
            else:
                raise TypeError('Parameter \'substring\' should be either a string or a list of strings. '
                                'A list containing non-strings was given)')
        else:
            raise TypeError(f'Parameter \'substring\' should be either a string or a list of strings '
                            f'({type(substring)} given)')

        prefix = '(?:.* )?' if exact else '.*'
        postfix = '(?: .*)?' if exact else '.*'
        super().__init__(f'^{prefix}({regexp_for_substring}){postfix}$')

    @staticmethod
    def validate_strings_list(strings):
        return all(map(lambda element: isinstance(element, str), strings))


class _HasExactWordTrigger(_HasSubstringTrigger):
    def __init__(self, word: Union[str, List[str]]):
        try:
            super().__init__(word, exact=True)
        except TypeError:
            raise TypeError(f'Parameter \'word\' should be either a string or a list of strings '
                            f'({type(word)} given)')


class TextTriggers(DictEnum):
    regexp = _RegExpTrigger
    has_substring = _HasSubstringTrigger
    has_exact_word = _HasExactWordTrigger
