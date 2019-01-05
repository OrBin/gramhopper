import json
from .configuration import users_file_path


class UsersHelper:

    def __init__(self, file_path: str = None):
        if file_path is not None:
            self.file_path = file_path
        else:
            self.file_path = users_file_path()

        self._users = {}
        self.load_users()

    def load_users(self, force: bool = False):
        if force or len(self._users) == 0:
            with open(self.file_path, 'r') as f:
                self._users = json.load(f)

    def get_user_id_by_nickname(self, nickname: str):
        return self._users[nickname]


default_users_helper = UsersHelper()