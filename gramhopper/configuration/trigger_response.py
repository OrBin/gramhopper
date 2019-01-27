from typing import Union
from ..triggers.basic_triggers import BaseTrigger
from ..responses.basic_responses import BaseResponse


TriggerResponse = Union[BaseTrigger, BaseResponse]
