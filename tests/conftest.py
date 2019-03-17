from datetime import datetime
from pytest import fixture
from telegram import Message, User, Chat, Update


@fixture(scope='module')
def update():
    return Update(0, Message(0, User(0, 'Testuser', False), datetime.now(),
                             Chat(0, 'private')))

