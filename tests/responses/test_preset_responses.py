import itertools
from typing import Union, List
import pytest
from flaky import flaky
from ...gramhopper.responses.preset_responses import _PresetDocumentResponse, \
    _PresetMessageResponse, _PresetReplyResponse
from . import FLAKY_MAX_RUNS, FLAKY_MIN_PASSES, delay_rerun


RESPONSE_PAYLOADS = [None, {}, {'key': 'value'}]


def is_acceptable(str_to_check: str, acceptable_string_or_strings: Union[str, List[str]]):
    if isinstance(acceptable_string_or_strings, list):
        return str_to_check in acceptable_string_or_strings

    return str_to_check == acceptable_string_or_strings


@pytest.mark.parametrize('payload', RESPONSE_PAYLOADS)
@flaky(max_runs=FLAKY_MAX_RUNS, min_passes=FLAKY_MIN_PASSES, rerun_filter=delay_rerun)
@pytest.mark.usefixtures('bot', 'bot_chat_id', 'generate_new_update')
class TestPresetResponsesWithParameterMatrices:

    SINGLE_PRESET_TEXT = 'one'
    MULTIPLE_PRESET_TEXTS = ['two', 'three']
    RESPONSE_PRESET_TEXTS = [SINGLE_PRESET_TEXT, MULTIPLE_PRESET_TEXTS]
    PAYLOADS_PRESET_RESPONSES_MATRIX = itertools.product(RESPONSE_PAYLOADS, RESPONSE_PRESET_TEXTS)
    DOCUMENT_URL = 'https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif'

    @pytest.mark.parametrize('preset_response', RESPONSE_PRESET_TEXTS)
    def test_preset_message_response(self, bot, bot_chat_id, generate_new_update, payload, preset_response):
        response = _PresetMessageResponse(preset_response)
        update = generate_new_update(chat_id=bot_chat_id)

        message = response.respond(bot, update, payload)
        assert message
        assert is_acceptable(message.text, preset_response)

    @pytest.mark.parametrize('preset_response', RESPONSE_PRESET_TEXTS)
    def test_preset_reply_response(self, bot, bot_chat_id, generate_new_update, payload, preset_response):
        response = _PresetReplyResponse(preset_response)
        message_to_reply_to = bot.send_message(chat_id=bot_chat_id, text='Message to reply to')
        update = generate_new_update(chat_id=bot_chat_id, message_id=message_to_reply_to.message_id)

        message = response.respond(bot, update, payload)
        assert message
        assert is_acceptable(message.text, preset_response)
        assert message.reply_to_message.message_id == message_to_reply_to.message_id

    def test_preset_document_response(self, bot, bot_chat_id, generate_new_update, payload):
        response = _PresetDocumentResponse(self.DOCUMENT_URL)
        update = generate_new_update(chat_id=bot_chat_id)

        message = response.respond(bot, update, payload)
        assert message
        assert message.document


class TestPresetTextResponse:

    SINGLE_PRESET_TEXT = 'one'
    MULTIPLE_PRESET_TEXTS = ['two', 'three']
    FLAKY_MAX_RUNS_FOR_RANDOMNESS = 20
    FLAKY_MIN_PASSES_FOR_RANDOMNESS = 1

    def test_get_response_text_from_single_preset_text(self):
        # _PresetTextResponse is abstract, so we're using _PresetMessageResponse to test it.
        response = _PresetMessageResponse(self.SINGLE_PRESET_TEXT)
        assert response.get_response_text() == self.SINGLE_PRESET_TEXT

    @pytest.mark.parametrize('preset_index', range(len(MULTIPLE_PRESET_TEXTS)))
    @flaky(max_runs=FLAKY_MAX_RUNS_FOR_RANDOMNESS, min_passes=FLAKY_MIN_PASSES_FOR_RANDOMNESS)
    def test_get_response_text_from_multiple_preset_texts(self, preset_index):
        # _PresetTextResponse is abstract, so we're using _PresetMessageResponse to test it.
        response = _PresetMessageResponse(self.MULTIPLE_PRESET_TEXTS)
        assert response.get_response_text() == self.MULTIPLE_PRESET_TEXTS[preset_index]
