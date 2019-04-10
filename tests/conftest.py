"""
This file contains global fixtures to use broadly on tests.
Read more here: https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions
"""

from datetime import datetime
from os import getenv
from pytest import fixture
from telegram import Message, User, Chat, Update, Bot


PUBLIC_TEST_BOT_PARAMETERS = {
    'token': '796912871:AAEc8dtCAmj4Jf4uht5dMfUWJCqOh8RDvAc',
    'chat_id': '-240130726',  # This is a dedicated group for testing
}


@fixture(scope='module')
def update() -> Update:
    """
    Creates a dummy update fixture.
    :return: a dummy update fixture
    """
    return _generate_new_update_impl()


@fixture(scope='module')
def generate_new_update():
    """
    Returns a generator function for new updates
    :return: an updates generator function
    """
    return _generate_new_update_impl


# pylint: disable=too-many-arguments
def _generate_new_update_impl(update_id=0,
                              message_id=0,
                              user_id=0,
                              user_first_name='Testuser',
                              user_is_bot=False,
                              message_date=None,
                              chat_id=0,
                              chat_type='private',
                              message_text=None) -> Update:

    if not message_date:
        message_date = datetime.now()

    return Update(update_id,
                  Message(message_id,
                          User(user_id, user_first_name, user_is_bot),
                          message_date,
                          Chat(chat_id, chat_type),
                          text=message_text))


def _get_bot_parameter(parameter_name: str) -> str:
    value = getenv(parameter_name.upper())

    if value:
        return value

    return PUBLIC_TEST_BOT_PARAMETERS[parameter_name]


@fixture(scope='module')
def bot() -> Bot:
    """
    Creates a valid bot instance, with a token from 'TOKEN' environment variable if exists,
    or the default one from PUBLIC_TEST_BOT_PARAMETERS otherwise.
    :return: a bot instance
    """
    return Bot(_get_bot_parameter('token'))


@fixture(scope='module')
def bot_chat_id() -> str:
    """
    Returns a chat id from 'CHAT_ID' environment variable if exists,
    or the default one from PUBLIC_TEST_BOT_PARAMETERS otherwise.
    :return: a chat id
    """
    return _get_bot_parameter('chat_id')
