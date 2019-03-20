from ..dict_enum import DictEnum
from .preset_responses import PresetResponses
from .match_responses import MatchResponses


class Responses(DictEnum):
    """A high-level class for all responses"""

    match = MatchResponses
    """Regexp-based responses. See more in :class:`MatchResponses`."""

    preset = PresetResponses
    """Preset responses. See more in :class:`PresetResponses`."""
