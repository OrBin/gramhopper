import pytest
from ...gramhopper.responses.preset_responses import _PresetTextResponse, \
    _PresetDocumentResponse, _PresetMessageResponse, _PresetReplyResponse


@pytest.mark.usefixtures('bot')
@pytest.mark.usefixtures('chat_id')
class TestPresetMessageResponse:

    SINGLE_PRESET_TEXT = 'one'
    MULTIPLE_PRESET_TEXTS = ['two', 'three']

    @pytest.mark.usefixtures('generate_new_update')
    def test_single_preset_message(self, bot, chat_id, generate_new_update):
        response = _PresetMessageResponse(self.SINGLE_PRESET_TEXT)

        update = generate_new_update(chat_id=chat_id)
        possible_values_for_payload = [None, {}, {'key': 'value'}]

        for payload in possible_values_for_payload:
            message = response.respond(bot, update, payload)
            assert message
            assert message.text == self.SINGLE_PRESET_TEXT

    @pytest.mark.usefixtures('generate_new_update')
    def test_multiple_preset_messages(self, bot, chat_id, generate_new_update):
        response = _PresetMessageResponse(self.MULTIPLE_PRESET_TEXTS)

        update = generate_new_update(chat_id=chat_id)
        possible_values_for_payload = [None, {}, {'key': 'value'}]

        for payload in possible_values_for_payload:
            message = response.respond(bot, update, payload)
            assert message
            assert message.text in self.MULTIPLE_PRESET_TEXTS
