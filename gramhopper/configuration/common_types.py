from typing import Union, Dict
from ..triggers.basic_triggers import BaseTrigger
from ..responses.basic_responses import BaseResponse


TriggerResponse = Union[BaseTrigger, BaseResponse]
GlobalsDict = Dict[str, TriggerResponse]
