from datetime import datetime
from pytest import fixture
from telegram import Message, User, Chat, Update
from ...gramhopper.triggers.text_triggers import _RegExpTrigger


@fixture(scope='module')
def update():
    return Update(0, Message(0, User(0, 'Testuser', False), datetime.now(),
                             Chat(0, 'private')))


def test_regexp_trigger(update):
    EMAIL_PATTERN = r'^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$'
    trigger = _RegExpTrigger(EMAIL_PATTERN)

    # Assuring that the regexp matches the message text
    update.message.text = 'user@example.com'
    result = trigger.check_trigger(update)
    assert result.should_respond
    assert 'match' in result.response_payload
    match = result.response_payload['match']
    assert match[0] == 'user'
    assert match[1] == 'example'
    assert match[2] == 'com'

    # Assuring that the regexp doesn't match the message text
    update.message.text = ''
    result = trigger.check_trigger(update)
    assert not result.should_respond
    assert result.response_payload == {}
