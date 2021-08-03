from pathlib import Path


__version__ = '0.1.0'


def get_home_path():
    return Path.home() / '.pyutils'
