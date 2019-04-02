import pytest
from time import sleep
from ...gramhopper.triggers.text_triggers import _HasExactWordTrigger
from ...gramhopper.triggers.event_streak_trigger import EventStreakTrigger


@pytest.mark.usefixtures('generate_new_update')
class TestEventStreakTrigger:
    COUNTING_MESSAGE_TEXT = 'count'
    RESETTING_MESSAGE_TEXT = 'reset'
    DO_NOTHING_MESSAGE_TEXT = 'nothing'
    COUNTING_TRIGGER = _HasExactWordTrigger(word=COUNTING_MESSAGE_TEXT)
    RESETTING_TRIGGER = _HasExactWordTrigger(word=RESETTING_MESSAGE_TEXT)

    def test_triggered_streak(self, generate_new_update):
        trigger = EventStreakTrigger(streak_timeout_sec=1,
                                     event_count=3,
                                     counting_event_trigger=self.COUNTING_TRIGGER,
                                     resetting_event_trigger=self.RESETTING_TRIGGER)

        update = generate_new_update(message_text=self.COUNTING_MESSAGE_TEXT)
        assert not trigger.check_trigger(update).should_respond

        update = generate_new_update(message_text=self.COUNTING_MESSAGE_TEXT)
        assert not trigger.check_trigger(update).should_respond

        update = generate_new_update(message_text=self.DO_NOTHING_MESSAGE_TEXT)
        assert not trigger.check_trigger(update).should_respond

        update = generate_new_update(message_text=self.COUNTING_MESSAGE_TEXT)
        assert trigger.check_trigger(update).should_respond

    def test_broken_streak(self, generate_new_update):
        trigger = EventStreakTrigger(streak_timeout_sec=1,
                                     event_count=3,
                                     counting_event_trigger=self.COUNTING_TRIGGER,
                                     resetting_event_trigger=self.RESETTING_TRIGGER)

        update = generate_new_update(message_text=self.COUNTING_MESSAGE_TEXT)
        assert not trigger.check_trigger(update).should_respond

        update = generate_new_update(message_text=self.COUNTING_MESSAGE_TEXT)
        assert not trigger.check_trigger(update).should_respond

        update = generate_new_update(message_text=self.RESETTING_MESSAGE_TEXT)
        assert not trigger.check_trigger(update).should_respond

        update = generate_new_update(message_text=self.COUNTING_MESSAGE_TEXT)
        assert not trigger.check_trigger(update).should_respond

    def test_no_enough_events_for_streak(self, generate_new_update):
        trigger = EventStreakTrigger(streak_timeout_sec=1,
                                     event_count=3,
                                     counting_event_trigger=self.COUNTING_TRIGGER,
                                     resetting_event_trigger=self.RESETTING_TRIGGER)

        update = generate_new_update(message_text=self.COUNTING_MESSAGE_TEXT)
        assert not trigger.check_trigger(update).should_respond

        update = generate_new_update(message_text=self.COUNTING_MESSAGE_TEXT)
        assert not trigger.check_trigger(update).should_respond

    def test_timed_out_streak(self, generate_new_update):
        trigger = EventStreakTrigger(streak_timeout_sec=0.2,
                                     event_count=3,
                                     counting_event_trigger=self.COUNTING_TRIGGER,
                                     resetting_event_trigger=self.RESETTING_TRIGGER)

        update = generate_new_update(message_text=self.COUNTING_MESSAGE_TEXT)
        assert not trigger.check_trigger(update).should_respond

        update = generate_new_update(message_text=self.COUNTING_MESSAGE_TEXT)
        assert not trigger.check_trigger(update).should_respond

        sleep(0.2)

        update = generate_new_update(message_text=self.COUNTING_MESSAGE_TEXT)
        assert not trigger.check_trigger(update).should_respond
