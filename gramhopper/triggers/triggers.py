from ..dict_enum import DictEnum
from .filter_triggers import FilterTriggers
from .text_triggers import TextTriggers
from .event_streak_trigger import EventStreakTrigger


class Triggers(DictEnum):
    text = TextTriggers
    filter = FilterTriggers
    event_streak = EventStreakTrigger
