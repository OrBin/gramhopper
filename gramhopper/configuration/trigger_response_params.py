from typing import NamedTuple, Dict, Type
from .triggers_reponses_parsers import BaseParser


class TriggerResponseParams(NamedTuple):
    key: str
    globals: Dict
    parser: Type[BaseParser]
