import pytest
from ...gramhopper.triggers.text_triggers import _RegExpTrigger, \
    _HasSubstringTrigger, _HasExactWordTrigger


@pytest.mark.usefixtures('update')
class TestRegexpTrigger:
    def test_regexp_trigger(self, update):
        EMAIL_PATTERN = r'^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$'
        trigger = _RegExpTrigger(EMAIL_PATTERN)

        # Assuring that the regexp matches the message text
        update.message.text = 'user@example.com'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 3
        assert match[0] == 'user'
        assert match[1] == 'example'
        assert match[2] == 'com'

        # Assuring that the regexp doesn't match the message text
        update.message.text = 'This is not an email address'
        result = trigger.check_trigger(update)
        assert not result.should_respond
        assert result.response_payload == {}


@pytest.mark.usefixtures('update')
class TestSubstringTrigger:
    def test_single_substring_exact(self, update):
        substring = 'ello'
        trigger = _HasSubstringTrigger(substring=substring, exact=True)

        update.message.text = 'ello'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] == substring

        update.message.text = 'hello'
        result = trigger.check_trigger(update)
        assert not result.should_respond
        assert result.response_payload == {}

    def test_single_substring_not_exact(self, update):
        substring = 'ello'
        trigger = _HasSubstringTrigger(substring=substring, exact=False)

        update.message.text = 'ello'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] == substring

        update.message.text = 'yellow'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] == substring

        update.message.text = 'goodbye'
        result = trigger.check_trigger(update)
        assert not result.should_respond
        assert result.response_payload == {}

    def test_multiple_substrings_exact(self, update):
        substrings = ['yellow', 'fellow']
        trigger = _HasSubstringTrigger(substring=substrings, exact=True)

        update.message.text = 'yellow'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] in substrings

        update.message.text = 'fellow'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] in substrings

        update.message.text = 'yellowstone'
        result = trigger.check_trigger(update)
        assert not result.should_respond
        assert result.response_payload == {}

    def test_multiple_substrings_not_exact(self, update):
        substrings = ['yellow', 'ello']
        trigger = _HasSubstringTrigger(substring=substrings, exact=False)

        update.message.text = 'yellow'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] in substrings

        update.message.text = 'fellow'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] in substrings

        update.message.text = 'goodbye'
        result = trigger.check_trigger(update)
        assert not result.should_respond
        assert result.response_payload == {}


@pytest.mark.usefixtures('update')
class TestExactWordTrigger:
    def test_single_substring_exact(self, update):
        word = 'ello'
        trigger = _HasExactWordTrigger(word=word)

        update.message.text = 'ello'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] == word

        update.message.text = 'hello'
        result = trigger.check_trigger(update)
        assert not result.should_respond
        assert result.response_payload == {}

    def test_multiple_substrings_exact(self, update):
        words = ['yellow', 'fellow']
        trigger = _HasExactWordTrigger(word=words)

        update.message.text = 'yellow'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] in words

        update.message.text = 'fellow'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] in words

        update.message.text = 'yellowstone'
        result = trigger.check_trigger(update)
        assert not result.should_respond
        assert result.response_payload == {}
