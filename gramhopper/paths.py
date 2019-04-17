from pathlib import Path


CONFIG_DIR = Path(Path.home(), '.gramhopper/')
TOKEN_FILE_NAME = 'token.txt'
DEFAULT_RULES_FILE_NAME = 'rules.yml'
USERS_FILE_NAME = 'users.json'
LOG_FILE_NAME = 'gramhopper.log'


def token_file_path():
    return Path(CONFIG_DIR, TOKEN_FILE_NAME)


def default_rules_file_path():
    return Path(CONFIG_DIR, DEFAULT_RULES_FILE_NAME)


def users_file_path():
    return Path(CONFIG_DIR, USERS_FILE_NAME)


def log_file_path(file_name=LOG_FILE_NAME):
    return Path(CONFIG_DIR, file_name)
