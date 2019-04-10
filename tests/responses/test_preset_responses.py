import pytest
from flaky import flaky
from ...gramhopper.responses.preset_responses import _PresetTextResponse, \
    _PresetDocumentResponse, _PresetMessageResponse, _PresetReplyResponse

FLAKY_MAX_RUNS = 5
FLAKY_MIN_PASSES = 1

@pytest.mark.usefixtures('bot')
@pytest.mark.usefixtures('chat_id')
class TestPresetMessageResponse:

    SINGLE_PRESET_TEXT = 'one'
    MULTIPLE_PRESET_TEXTS = ['two', 'three']

    def _test_single_preset_message(self, bot, chat_id, generate_new_update, payload):
        response = _PresetMessageResponse(self.SINGLE_PRESET_TEXT)
        update = generate_new_update(chat_id=chat_id)

        message = response.respond(bot, update, payload)
        assert message
        assert message.text == self.SINGLE_PRESET_TEXT

    def _test_multiple_preset_messages(self, bot, chat_id, generate_new_update, payload):
        response = _PresetMessageResponse(self.MULTIPLE_PRESET_TEXTS)
        update = generate_new_update(chat_id=chat_id)

        message = response.respond(bot, update, payload)
        assert message
        assert message.text in self.MULTIPLE_PRESET_TEXTS

    @flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES)
    @pytest.mark.usefixtures('generate_new_update')
    def test_single_preset_message_with_none_payload(self, bot, chat_id, generate_new_update):
        self._test_single_preset_message(bot, chat_id, generate_new_update, None)

    @flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES)
    @pytest.mark.usefixtures('generate_new_update')
    def test_single_preset_message_with_empty_payload(self, bot, chat_id, generate_new_update):
        self._test_single_preset_message(bot, chat_id, generate_new_update, {})

    @flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES)
    @pytest.mark.usefixtures('generate_new_update')
    def test_single_preset_message_with_some_payload(self, bot, chat_id, generate_new_update):
        self._test_single_preset_message(bot, chat_id, generate_new_update, {'key': 'value'})

    @flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES)
    @pytest.mark.usefixtures('generate_new_update')
    def test_multiple_preset_messages_with_none_payload(self, bot, chat_id, generate_new_update):
        self._test_single_preset_message(bot, chat_id, generate_new_update, None)

    @flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES)
    @pytest.mark.usefixtures('generate_new_update')
    def test_multiple_preset_messages_with_empty_payload(self, bot, chat_id, generate_new_update):
        self._test_single_preset_message(bot, chat_id, generate_new_update, {})

    @flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES)
    @pytest.mark.usefixtures('generate_new_update')
    def test_multiple_preset_messages_with_some_payload(self, bot, chat_id, generate_new_update):
        self._test_single_preset_message(bot, chat_id, generate_new_update, {'key': 'value'})

    @flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES)
    @pytest.mark.usefixtures('generate_new_update')
    def test_multiple_preset_messages(self, bot, chat_id, generate_new_update):
        possible_values_for_payload = [None, {}, {'key': 'value'}]
        for payload in possible_values_for_payload:
            self._test_multiple_preset_messages(bot, chat_id, generate_new_update, payload)


@pytest.mark.usefixtures('bot')
@pytest.mark.usefixtures('chat_id')
class TestPresetReplyResponse:

    SINGLE_PRESET_TEXT = 'one'
    MULTIPLE_PRESET_TEXTS = ['two', 'three']

    def _test_single_preset_reply(self, bot, chat_id, generate_new_update, payload):
        response = _PresetReplyResponse(self.SINGLE_PRESET_TEXT)
        message_to_reply_to = bot.send_message(chat_id=chat_id, text='Message to reply to')
        update = generate_new_update(chat_id=chat_id, message_id=message_to_reply_to.message_id)

        message = response.respond(bot, update, payload)
        assert message
        assert message.text == self.SINGLE_PRESET_TEXT
        assert message.reply_to_message.message_id == message_to_reply_to.message_id

    def _test_multiple_preset_replies(self, bot, chat_id, generate_new_update, payload):
        response = _PresetReplyResponse(self.MULTIPLE_PRESET_TEXTS)
        message_to_reply_to = bot.send_message(chat_id=chat_id, text='Message to reply to')
        update = generate_new_update(chat_id=chat_id, message_id=message_to_reply_to.message_id)

        message = response.respond(bot, update, payload)
        assert message
        assert message.text in self.MULTIPLE_PRESET_TEXTS
        assert message.reply_to_message.message_id == message_to_reply_to.message_id

    @flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES)
    @pytest.mark.usefixtures('generate_new_update')
    def test_single_preset_reply_with_none_payload(self, bot, chat_id, generate_new_update):
        self._test_single_preset_reply(bot, chat_id, generate_new_update, None)


    @flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES)
    @pytest.mark.usefixtures('generate_new_update')
    def test_single_preset_reply_with_empty_payload(self, bot, chat_id, generate_new_update):
        self._test_single_preset_reply(bot, chat_id, generate_new_update, {})

    @flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES)
    @pytest.mark.usefixtures('generate_new_update')
    def test_single_preset_reply_with_some_payload(self, bot, chat_id, generate_new_update):
        self._test_single_preset_reply(bot, chat_id, generate_new_update, {'key': 'value'})

    @flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES)
    @pytest.mark.usefixtures('generate_new_update')
    def test_multiple_preset_replies_with_none_payload(self, bot, chat_id, generate_new_update):
        self._test_single_preset_reply(bot, chat_id, generate_new_update, None)

    @flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES)
    @pytest.mark.usefixtures('generate_new_update')
    def test_multiple_preset_replies_with_empty_payload(self, bot, chat_id, generate_new_update):
        self._test_single_preset_reply(bot, chat_id, generate_new_update, {})

    @flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES)
    @pytest.mark.usefixtures('generate_new_update')
    def test_multiple_preset_replies_with_some_payload(self, bot, chat_id, generate_new_update):
        self._test_single_preset_reply(bot, chat_id, generate_new_update, {'key': 'value'})

    @flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES)
    @pytest.mark.usefixtures('generate_new_update')
    def test_multiple_preset_replies(self, bot, chat_id, generate_new_update):
        possible_values_for_payload = [None, {}, {'key': 'value'}]
        for payload in possible_values_for_payload:
            self._test_multiple_preset_replies(bot, chat_id, generate_new_update, payload)
