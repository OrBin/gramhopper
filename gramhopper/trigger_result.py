from typing import NamedTuple


class TriggerResult(NamedTuple):
    should_respond: bool
    response_payload: dict = {}
