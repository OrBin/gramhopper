import pytest
from flaky import flaky
from ...gramhopper.responses.match_responses import _MatchMessageResponse, _MatchReplyResponse
from . import FLAKY_MAX_RUNS, FLAKY_MIN_PASSES, delay_rerun


OUTPUT_TEMPLATE = 'Goodbye, {0} {1}'
MATCH_PARAMS = ('Ruby', 'Tuesday')
EXPECTED_RESPONSE = 'Goodbye, Ruby Tuesday'


@flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES, rerun_filter=delay_rerun)
@pytest.mark.usefixtures('bot', 'bot_chat_id', 'generate_new_update')
class TestMatchMessageResponse:
    def test_match_message_response(self, bot, bot_chat_id, generate_new_update):
        response = _MatchMessageResponse(OUTPUT_TEMPLATE)
        update = generate_new_update(chat_id=bot_chat_id)

        payload = {'match': MATCH_PARAMS}
        message = response.respond(bot, update, payload)
        assert message
        assert message.text == EXPECTED_RESPONSE


@flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES, rerun_filter=delay_rerun)
@pytest.mark.usefixtures('bot', 'bot_chat_id', 'generate_new_update')
class TestMatchReplyResponse:
    def test_match_reply_response(self, bot, bot_chat_id, generate_new_update):
        response = _MatchReplyResponse(OUTPUT_TEMPLATE)
        message_to_reply_to = bot.send_message(chat_id=bot_chat_id, text='Message to reply to')
        update = generate_new_update(chat_id=bot_chat_id, message_id=message_to_reply_to.message_id)

        payload = {'match': MATCH_PARAMS}
        message = response.respond(bot, update, payload)
        assert message
        assert message.text == EXPECTED_RESPONSE
        assert message.reply_to_message.message_id == message_to_reply_to.message_id


class TestMatchTextResponse:
    def test_get_response_text_from_single_preset_text(self):
        # _MatchTextResponse is abstract, so we're using _MatchMessageResponse to test it.
        response = _MatchMessageResponse(OUTPUT_TEMPLATE)
        payload = {'match': MATCH_PARAMS}

        assert response.build_response_text(payload) == EXPECTED_RESPONSE
