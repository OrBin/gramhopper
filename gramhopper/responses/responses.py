from ..dict_enum import DictEnum
from .preset_responses import PresetResponses
from .match_responses import MatchResponses

class Responses(DictEnum):
    preset = PresetResponses
    match = MatchResponses
