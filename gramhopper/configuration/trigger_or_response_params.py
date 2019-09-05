from typing import Dict
from dataclasses import dataclass
from .common_types import GlobalsDict
from .trigger_or_response_parser import TriggerOrResponseParser
from ..triggers.basic_triggers import BaseTrigger
from ..responses.basic_responses import BaseResponse
from ..responses import Responses
from ..triggers import Triggers


@dataclass
class TriggerOrResponseParams:
    singular_key: str
    global_elements: GlobalsDict
    parser: TriggerOrResponseParser

    @property
    def plural_key(self):
        return self.singular_key + 's'


@dataclass
class TriggerParams(TriggerOrResponseParams):
    def __init__(self, global_elements: Dict[str, BaseTrigger]):
        super().__init__(singular_key='trigger',
                         global_elements=global_elements,
                         parser=TriggerOrResponseParser(Triggers, BaseTrigger))


@dataclass
class ResponseParams(TriggerOrResponseParams):
    def __init__(self, global_elements: Dict[str, BaseResponse]):
        super().__init__(singular_key='response',
                         global_elements=global_elements,
                         parser=TriggerOrResponseParser(Responses, BaseResponse))
