from pathlib import Path
from sys import platform
import os


_LINUX_GLOBAL_CONFIGURATION_DIR = '/etc/gramhopper'
_LINUX_USER_CONFIGURATION_DIR = Path(Path.home(), '.gramhopper/')


def configuration_dir():
    if platform == "linux" or platform == "linux2":
        if os.access(_LINUX_GLOBAL_CONFIGURATION_DIR, os.R_OK):
            return _LINUX_GLOBAL_CONFIGURATION_DIR
        else:
            return _LINUX_USER_CONFIGURATION_DIR
    else:
        raise NotImplementedError('Running on OS other than linux is currently unsupported')
