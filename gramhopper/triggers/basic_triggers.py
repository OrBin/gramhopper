import abc
from typing import Optional
from telegram import Update
from .trigger_result import TriggerResult
from ..representable import Representable


class BaseTrigger(abc.ABC, Representable):

    @abc.abstractmethod
    def check_trigger(self, update: Update) -> TriggerResult:
        pass

    def __and__(self, other):
        return MergedTrigger(self, and_trigger=other)

    def __or__(self, other):
        return MergedTrigger(self, or_trigger=other)

    def __invert__(self):
        return InvertedTrigger(self)


class MergedTrigger(BaseTrigger):
    """Represents a trigger consisting of two other triggers.

    Args:
        base_trigger: Base trigger of the merged trigger
        and_trigger: Optional trigger to "and" with base_trigger.
            Mutually exclusive with or_trigger.
        or_trigger: Optional trigger to "or" with base_trigger.
            Mutually exclusive with and_trigger.

    """

    def __init__(self,
                 base_trigger: BaseTrigger,
                 and_trigger: BaseTrigger = None,
                 or_trigger: BaseTrigger = None):
        super().__init__()
        self.base_trigger = base_trigger
        self.and_trigger = and_trigger
        self.or_trigger = or_trigger

    def check_trigger(self, update: Update) -> Optional[TriggerResult]:
        if self.and_trigger:
            return self.check_trigger_and(update)

        if self.or_trigger:
            return self.check_trigger_or(update)

        return None

    def check_trigger_and(self, update: Update) -> TriggerResult:
        base_result = self.base_trigger.check_trigger(update)
        and_result = self.and_trigger.check_trigger(update)

        if base_result.should_respond and and_result.should_respond:
            merged_payload = self.merge_payloads(base_result, and_result)
            return TriggerResult(should_respond=True,
                                 response_payload=merged_payload)

        return TriggerResult(should_respond=False)

    def check_trigger_or(self, update: Update) -> TriggerResult:
        base_result = self.base_trigger.check_trigger(update)
        or_result = self.or_trigger.check_trigger(update)

        should_respond = False
        response_payload = {}
        if base_result.should_respond:
            should_respond = True
            if or_result.should_respond:
                response_payload = self.merge_payloads(base_result, or_result)
            else:
                response_payload = base_result.response_payload
        elif or_result.should_respond:
            should_respond = True
            response_payload = or_result.response_payload

        return TriggerResult(should_respond, response_payload)  # pytype: disable=wrong-arg-count

    @staticmethod
    def merge_payloads(first: TriggerResult, second: TriggerResult) -> dict:
        return {**first.response_payload, **second.response_payload}


class InvertedTrigger(BaseTrigger):
    """Represents a trigger that has been inverted.
    Args:
        original_trigger: The trigger to invert.
    """

    def __init__(self, original_trigger: BaseTrigger):
        super().__init__()
        self.original_trigger = original_trigger

    def check_trigger(self, update: Update) -> TriggerResult:
        original_result = self.original_trigger.check_trigger(update)
        return TriggerResult(should_respond=not original_result.should_respond)
