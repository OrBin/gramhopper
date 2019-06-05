from datetime import datetime
from typing import Optional
from telegram import Update
from .trigger_result import TriggerResult
from .basic_triggers import BaseTrigger


class EventStreakTrigger(BaseTrigger):
    """
    Event-streak trigger. This is used to trigger a rule in a case of a streak of events,
    for example when a certain phrase is written a few times in a row.

    This trigger gets a defined trigger as a "counting" event and optionally another one as a
    "resetting" event (to stop counting).
    It also gets the count of events to be considered a streak, and the timeout of the streak (the
    allowed time period between the first event and the last event in the streak.
    """

    def __init__(self,
                 streak_timeout_sec: float,
                 event_count: int,
                 counting_event_trigger: BaseTrigger,
                 resetting_event_trigger: Optional[BaseTrigger] = None):
        """
        Constructs the trigger.

        :param streak_timeout_sec: The allowed time period between the first event and the last \
        event in the streak
        :param event_count: The count of events to be considered a streak
        :param counting_event_trigger: A trigger to identify an event that counts towards the streak
        :param resetting_event_trigger: A trigger to identify an event that resets the streak
        """
        super().__init__()
        self.streak_timeout_sec = streak_timeout_sec
        self.event_count = event_count
        self.counting_event_trigger = counting_event_trigger

        if resetting_event_trigger is not None:
            self.resetting_event_trigger = resetting_event_trigger
        else:
            self.resetting_event_trigger = ~counting_event_trigger

        self.message_counter = 0
        self.streak_start_timestamp = 0

    def check_trigger(self, update: Update) -> TriggerResult:
        if self.counting_event_trigger.check_trigger(update).should_respond:
            now_timestamp = datetime.now().timestamp()

            if now_timestamp - self.streak_start_timestamp > self.streak_timeout_sec:
                self.reset_count()

            if self.message_counter == 0:
                self.streak_start_timestamp = datetime.now().timestamp()

            self.message_counter += 1

            if self.message_counter == self.event_count:
                self.reset_count()
                return TriggerResult(should_respond=True)

        elif self.resetting_event_trigger.check_trigger(update).should_respond:
            self.reset_count()

        return TriggerResult(should_respond=False)

    def reset_count(self):
        self.message_counter = 0
