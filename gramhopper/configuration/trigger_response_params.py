from typing import Dict, Type
from dataclasses import dataclass
from .globals_dict import GlobalsDict
from .triggers_reponses_parsers import BaseParser, TriggerParser, ResponseParser
from ..triggers.basic_triggers import BaseTrigger
from ..responses.basic_responses import BaseResponse


@dataclass
class TriggerResponseParams:
    singular_key: str
    global_elements: GlobalsDict
    parser: Type[BaseParser]

    @property
    def plural_key(self):
        return self.singular_key + 's'


@dataclass
class TriggerParams(TriggerResponseParams):
    def __init__(self, global_elements: Dict[str, BaseTrigger]):
        super().__init__(singular_key='trigger',
                         global_elements=global_elements,
                         parser=TriggerParser)


@dataclass
class ResponseParams(TriggerResponseParams):
    def __init__(self, global_elements: Dict[str, BaseResponse]):
        super().__init__(singular_key='response',
                         global_elements=global_elements,
                         parser=ResponseParser)
