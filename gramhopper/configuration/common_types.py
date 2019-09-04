from typing import Union, Dict
from ..triggers.basic_triggers import BaseTrigger
from ..responses.basic_responses import BaseResponse


TriggerOrResponse = Union[BaseTrigger, BaseResponse]
GlobalsDict = Dict[str, TriggerOrResponse]
