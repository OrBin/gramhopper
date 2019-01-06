from dataclasses import dataclass
from typing import Dict, Type
from .trigger_response import TriggerResponse
from .triggers_reponses_parsers import BaseParser, TriggerParser, ResponseParser
from ..triggers.basic_triggers import BaseTrigger
from ..responses.basic_responses import BaseResponse


@dataclass
class TriggerResponseParams:
    singular_key: str
    globals: Dict[str, TriggerResponse]
    parser: Type[BaseParser]

    @property
    def plural_key(self):
        return self.singular_key + 's'


@dataclass
class TriggerParams(TriggerResponseParams):
    def __init__(self, globals: Dict[str, BaseTrigger]):
        super().__init__(singular_key='trigger', globals=globals, parser=TriggerParser)


@dataclass
class ResponseParams(TriggerResponseParams):
    def __init__(self, globals: Dict[str, BaseResponse]):
        super().__init__(singular_key='response', globals=globals, parser=ResponseParser)
