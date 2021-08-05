from pathlib import Path
import json


def have_tests_failed(dir_name):
    """
    Returns:
        int : Based on its value, one of the following situations happened:

            - 0: Tests were successful.
            - 1: Tests failed.
            - 2: pycache directory does not exist.
    """
    # TODO: robustness still to be confirmed

    pycache_paths = list(Path(dir_name).glob('**/.pytest_cache'))
    if len(pycache_paths) == 0:
        return 2
    pycache_path = pycache_paths[0]

    # py cache does not exist
    if not pycache_path.exists():
        return 2

    # lastfailed file does not exist
    lastfailed_paths = list(pycache_path.glob('**/lastfailed'))
    if len(lastfailed_paths) == 0:
        return 0

    # lastfailed file exists
    lastfailed_path = lastfailed_paths[0]
    with open(lastfailed_path, 'r') as file:
        fail_info = json.load(file)

    return int(len(fail_info) > 0)
