"""
This file contains global fixtures to use broadly on tests.
Read more here: https://docs.pytest.org/en/latest/fixture.html#conftest-py-sharing-fixture-functions
"""

from datetime import datetime
from pytest import fixture
from telegram import Message, User, Chat, Update


@fixture(scope='module')
def update():
    return Update(0, Message(0, User(0, 'Testuser', False), datetime.now(),
                             Chat(0, 'private')))
