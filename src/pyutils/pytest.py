from pathlib import Path
import json


def have_tests_failed(dir_name):
    """
    Returns:
        int : Based on its value, one of the following situations happened:

            - 0: Tests were successful.
            - 1: Tests failed.
            - 2: pycache directory does not exist or tests were not performed.
    """
    # TODO: robustness still to be confirmed

    pycache_paths = list(Path(dir_name).glob('**/.pytest_cache'))
    if len(pycache_paths) == 0:
        return 2
    pycache_path = pycache_paths[0]

    # py cache does not exist
    if not pycache_path.exists():
        return 2

    # py cache exists, but tests were not run
    run_info = _read_info_from_json(list(pycache_path.glob('**/nodeids'))[0])
    if len(run_info) == 0:
        return 2

    # lastfailed file does not exist
    lastfailed_paths = list(pycache_path.glob('**/lastfailed'))
    if len(lastfailed_paths) == 0:
        return 0

    # lastfailed file exists
    fail_info = _read_info_from_json(lastfailed_paths[0])

    return int(len(fail_info) > 0)


def _read_info_from_json(filename):
    with open(filename, 'r') as file:
        info = json.load(file)

    return info
