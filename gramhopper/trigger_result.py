from dataclasses import dataclass, field


@dataclass
class TriggerResult:
    should_respond: bool
    response_payload: dict = field(default_factory=dict)
