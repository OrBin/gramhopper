import pytest
from ...gramhopper.triggers.text_triggers import _RegExpTrigger, \
    _HasSubstringTrigger, _HasExactWordTrigger

# pylint: disable=use-implicit-booleaness-not-comparison


@pytest.mark.usefixtures('update')
class TestRegexpTrigger:

    EMAIL_PATTERN = r'^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,})$'

    def test_message_matches(self, update):
        trigger = _RegExpTrigger(self.EMAIL_PATTERN)

        update.message.text = 'user@example1.com'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert result.response_payload
        assert isinstance(result.response_payload, dict)
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 3
        assert match[0] == 'user'
        assert match[1] == 'example1'
        assert match[2] == 'com'

    def test_message_does_not_match(self, update):
        trigger = _RegExpTrigger(self.EMAIL_PATTERN)

        update.message.text = 'This is not an email address'
        result = trigger.check_trigger(update)
        assert not result.should_respond
        assert result.response_payload == {}


@pytest.mark.usefixtures('update')
class TestSubstringTrigger:

    SINGLE_SUBSTRING = 'ello'
    MULTIPLE_SUBSTRINGS = ['yellow', 'ello']

    def test_single_substring_exact_matches(self, update):
        trigger = _HasSubstringTrigger(substring=self.SINGLE_SUBSTRING, exact=True)

        update.message.text = 'ello'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert result.response_payload
        assert isinstance(result.response_payload, dict)
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] == self.SINGLE_SUBSTRING

    def test_single_substring_exact_does_not_match(self, update):
        trigger = _HasSubstringTrigger(substring=self.SINGLE_SUBSTRING, exact=True)

        update.message.text = 'hello'
        result = trigger.check_trigger(update)
        assert not result.should_respond
        assert result.response_payload == {}

    def test_single_substring_not_exact_matches(self, update):
        trigger = _HasSubstringTrigger(substring=self.SINGLE_SUBSTRING, exact=False)

        update.message.text = 'ello'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert result.response_payload
        assert isinstance(result.response_payload, dict)
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] == self.SINGLE_SUBSTRING

        update.message.text = 'yellow'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert result.response_payload
        assert isinstance(result.response_payload, dict)
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] == self.SINGLE_SUBSTRING

    def test_single_substring_not_exact_does_not_match(self, update):
        trigger = _HasSubstringTrigger(substring=self.SINGLE_SUBSTRING, exact=False)

        update.message.text = 'goodbye'
        result = trigger.check_trigger(update)
        assert not result.should_respond
        assert result.response_payload == {}

    def test_multiple_substrings_exact_matches(self, update):
        trigger = _HasSubstringTrigger(substring=self.MULTIPLE_SUBSTRINGS, exact=True)

        update.message.text = 'yellow'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert result.response_payload
        assert isinstance(result.response_payload, dict)
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] in self.MULTIPLE_SUBSTRINGS

        update.message.text = 'ello'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert result.response_payload
        assert isinstance(result.response_payload, dict)
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] in self.MULTIPLE_SUBSTRINGS

    def test_multiple_substrings_exact_does_not_match(self, update):
        trigger = _HasSubstringTrigger(substring=self.MULTIPLE_SUBSTRINGS, exact=True)

        update.message.text = 'yellowstone'
        result = trigger.check_trigger(update)
        assert not result.should_respond
        assert result.response_payload == {}

    def test_multiple_substrings_not_exact_matches(self, update):
        trigger = _HasSubstringTrigger(substring=self.MULTIPLE_SUBSTRINGS, exact=False)

        update.message.text = 'yellow'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert result.response_payload
        assert isinstance(result.response_payload, dict)
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] in self.MULTIPLE_SUBSTRINGS

        update.message.text = 'fellow'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert result.response_payload
        assert isinstance(result.response_payload, dict)
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] in self.MULTIPLE_SUBSTRINGS

    def test_multiple_substrings_not_exact_does_not_match(self, update):
        trigger = _HasSubstringTrigger(substring=self.MULTIPLE_SUBSTRINGS, exact=False)

        update.message.text = 'goodbye'
        result = trigger.check_trigger(update)
        assert not result.should_respond
        assert result.response_payload == {}


@pytest.mark.usefixtures('update')
class TestExactWordTrigger:

    SINGLE_WORD = 'ello'
    MULTIPLE_WORDS = ['yellow', 'fellow']

    def test_single_substring_exact_matches(self, update):
        trigger = _HasExactWordTrigger(word=self.SINGLE_WORD)

        update.message.text = 'ello'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert result.response_payload
        assert isinstance(result.response_payload, dict)
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] == self.SINGLE_WORD

    def test_single_substring_exact_does_not_match(self, update):
        trigger = _HasExactWordTrigger(word=self.SINGLE_WORD)

        update.message.text = 'hello'
        result = trigger.check_trigger(update)
        assert not result.should_respond
        assert result.response_payload == {}

    def test_multiple_substrings_exact_matches(self, update):
        trigger = _HasExactWordTrigger(word=self.MULTIPLE_WORDS)

        update.message.text = 'yellow'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert result.response_payload
        assert isinstance(result.response_payload, dict)
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] in self.MULTIPLE_WORDS

        update.message.text = 'fellow'
        result = trigger.check_trigger(update)
        assert result.should_respond
        assert result.response_payload
        assert isinstance(result.response_payload, dict)
        assert 'match' in result.response_payload
        match = result.response_payload['match']
        assert len(match) == 1
        assert match[0] in self.MULTIPLE_WORDS

    def test_multiple_substrings_exact_does_not_match(self, update):
        trigger = _HasExactWordTrigger(word=self.MULTIPLE_WORDS)

        update.message.text = 'yellowstone'
        result = trigger.check_trigger(update)
        assert not result.should_respond
        assert result.response_payload == {}
