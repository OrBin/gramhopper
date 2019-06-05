import json
import os
from typing import Union
from .paths import users_file_path


class UsersHelper:

    def __init__(self, file_path: Union[os.PathLike, str, bytes] = None):
        if file_path is not None:
            self.file_path = file_path
        else:
            self.file_path = users_file_path()

        self._users = {}
        self.load_users()

    def load_users(self, force: bool = False):
        if force or not self._users:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    self._users = json.load(file)

    def get_user_id_by_nickname(self, nickname: str) -> int:
        return self._users[nickname]


DEFAULT_USERS_HELPER = UsersHelper()
