"""
This file contains global fixtures to use broadly on tests.
Read more here: https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions
"""

from datetime import datetime
from pytest import fixture
from telegram import Message, User, Chat, Update


# This fixture was copied from the tests in python-telegram-bot:
#
@fixture(scope='module')
def update():
    """
    Creates a dummy update fixture.
    This fixture was copied from the tests in python-telegram-bot:
    https://github.com/python-telegram-bot/python-telegram-bot/blob/b5891a6/tests/test_filters.py#L29
    :return: a dummy update fixture
    """
    return Update(0, Message(0, User(0, 'Testuser', False), datetime.now(),
                             Chat(0, 'private')))
