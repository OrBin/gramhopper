from pathlib import Path
from typing import Optional
from ruamel.yaml import YAML
from .paths import USERS_FILE_PATH


class UsersHelper:
    """ A helper for loading and reading users from the users file """

    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = Path(file_path) if file_path else USERS_FILE_PATH
        self.user_id_by_nickname = {}
        self.load_users()

    def load_users(self, force: bool = False):
        # Load only if forced to load or did not load yet
        if not force and self.user_id_by_nickname:
            return

        if not self.file_path.exists():
            return

        with self.file_path.open('r', encoding='utf-8') as stream:
            raw_users = YAML().load(stream)
            self.user_id_by_nickname = {user["nickname"]: user["id"] for user in raw_users["users"]}

    def get_user_id_by_nickname(self, nickname: str) -> int:
        return self.user_id_by_nickname[nickname]


DEFAULT_USERS_HELPER = UsersHelper()
