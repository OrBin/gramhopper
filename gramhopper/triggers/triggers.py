from .filter_triggers import FilterTriggers
from .text_triggers import TextTriggers
from .event_streak_trigger import EventStreakTrigger


class Triggers:
    text = TextTriggers
    filter = FilterTriggers
    event_streak = EventStreakTrigger
