"""
This file contains global fixtures to use broadly on tests.
Read more here: https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions
"""

from datetime import datetime
from pytest import fixture
from telegram import Message, User, Chat, Update


@fixture(scope='module')
def update():
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


def _generate_new_update_impl(update_id=0,
                              message_id=0,
                              user_id=0,
                              user_first_name='Testuser',
                              user_is_bot=False,
                              message_date=None,
                              chat_id=0,
                              chat_type='private'):

    if not message_date:
        message_date = datetime.now()

    return Update(update_id,
                  Message(message_id,
                          User(user_id, user_first_name, user_is_bot),
                          message_date,
                          Chat(chat_id, chat_type)))
