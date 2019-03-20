from ..dict_enum import DictEnum
from .filter_triggers import FilterTriggers
from .text_triggers import TextTriggers
from .event_streak_trigger import EventStreakTrigger


class Triggers(DictEnum):
    """A high-level class for all triggers"""

    event_streak = EventStreakTrigger
    """Event-streak trigger. See more in :class:`EventStreakTrigger`."""

    filter = FilterTriggers
    """Filter-based triggers. See more in :class:`FilterTriggers`."""

    text = TextTriggers
    """Text-based triggers. See more in :class:`TextTriggers`."""
