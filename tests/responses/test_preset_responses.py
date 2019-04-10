import time
import pytest
from flaky import flaky
from ...gramhopper.responses.preset_responses import _PresetTextResponse, \
    _PresetDocumentResponse, _PresetMessageResponse, _PresetReplyResponse


FLAKY_MAX_RUNS = 6
FLAKY_MIN_PASSES = 1


def delay_rerun(*args):  # pylint: disable=unused-argument
    time.sleep(2)
    return True


@flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES, rerun_filter=delay_rerun)
@pytest.mark.usefixtures('bot', 'bot_chat_id', 'generate_new_update')
class TestPresetMessageResponse:

    SINGLE_PRESET_TEXT = 'one'
    MULTIPLE_PRESET_TEXTS = ['two', 'three']

    def _test_single_preset_message(self, bot, bot_chat_id, generate_new_update, payload):
        response = _PresetMessageResponse(self.SINGLE_PRESET_TEXT)
        update = generate_new_update(chat_id=bot_chat_id)

        message = response.respond(bot, update, payload)
        assert message
        assert message.text == self.SINGLE_PRESET_TEXT

    def _test_multiple_preset_messages(self, bot, bot_chat_id, generate_new_update, payload):
        response = _PresetMessageResponse(self.MULTIPLE_PRESET_TEXTS)
        update = generate_new_update(chat_id=bot_chat_id)

        message = response.respond(bot, update, payload)
        assert message
        assert message.text in self.MULTIPLE_PRESET_TEXTS

    def test_single_preset_message_with_none_payload(self, bot, bot_chat_id, generate_new_update):
        self._test_single_preset_message(bot, bot_chat_id, generate_new_update, None)

    def test_single_preset_message_with_empty_payload(self, bot, bot_chat_id, generate_new_update):
        self._test_single_preset_message(bot, bot_chat_id, generate_new_update, {})

    def test_single_preset_message_with_some_payload(self, bot, bot_chat_id, generate_new_update):
        self._test_single_preset_message(bot, bot_chat_id, generate_new_update, {'key': 'value'})

    def test_multiple_preset_messages_with_none_payload(self, bot, bot_chat_id, generate_new_update):
        self._test_single_preset_message(bot, bot_chat_id, generate_new_update, None)

    def test_multiple_preset_messages_with_empty_payload(self, bot, bot_chat_id, generate_new_update):
        self._test_single_preset_message(bot, bot_chat_id, generate_new_update, {})

    def test_multiple_preset_messages_with_some_payload(self, bot, bot_chat_id, generate_new_update):
        self._test_single_preset_message(bot, bot_chat_id, generate_new_update, {'key': 'value'})


@flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES, rerun_filter=delay_rerun)
@pytest.mark.usefixtures('bot', 'bot_chat_id', 'generate_new_update')
class TestPresetReplyResponse:

    SINGLE_PRESET_TEXT = 'one'
    MULTIPLE_PRESET_TEXTS = ['two', 'three']

    def _test_single_preset_reply(self, bot, bot_chat_id, generate_new_update, payload):
        response = _PresetReplyResponse(self.SINGLE_PRESET_TEXT)
        message_to_reply_to = bot.send_message(chat_id=bot_chat_id, text='Message to reply to')
        update = generate_new_update(chat_id=bot_chat_id, message_id=message_to_reply_to.message_id)

        message = response.respond(bot, update, payload)
        assert message
        assert message.text == self.SINGLE_PRESET_TEXT
        assert message.reply_to_message.message_id == message_to_reply_to.message_id

    def _test_multiple_preset_replies(self, bot, bot_chat_id, generate_new_update, payload):
        response = _PresetReplyResponse(self.MULTIPLE_PRESET_TEXTS)
        message_to_reply_to = bot.send_message(chat_id=bot_chat_id, text='Message to reply to')
        update = generate_new_update(chat_id=bot_chat_id, message_id=message_to_reply_to.message_id)

        message = response.respond(bot, update, payload)
        assert message
        assert message.text in self.MULTIPLE_PRESET_TEXTS
        assert message.reply_to_message.message_id == message_to_reply_to.message_id

    def test_single_preset_reply_with_none_payload(self, bot, bot_chat_id, generate_new_update):
        self._test_single_preset_reply(bot, bot_chat_id, generate_new_update, None)

    def test_single_preset_reply_with_empty_payload(self, bot, bot_chat_id, generate_new_update):
        self._test_single_preset_reply(bot, bot_chat_id, generate_new_update, {})

    def test_single_preset_reply_with_some_payload(self, bot, bot_chat_id, generate_new_update):
        self._test_single_preset_reply(bot, bot_chat_id, generate_new_update, {'key': 'value'})

    def test_multiple_preset_replies_with_none_payload(self, bot, bot_chat_id, generate_new_update):
        self._test_single_preset_reply(bot, bot_chat_id, generate_new_update, None)

    def test_multiple_preset_replies_with_empty_payload(self, bot, bot_chat_id, generate_new_update):
        self._test_single_preset_reply(bot, bot_chat_id, generate_new_update, {})

    def test_multiple_preset_replies_with_some_payload(self, bot, bot_chat_id, generate_new_update):
        self._test_single_preset_reply(bot, bot_chat_id, generate_new_update, {'key': 'value'})
