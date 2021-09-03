import json
from pyutils import get_home_path


def get_auth_filepath(filename):
    return get_home_path() / filename


def get_secrets(filename):
    filepath = get_auth_filepath(filename)
    with open(filepath, 'r') as file:
        data = json.load(file)

    return data
