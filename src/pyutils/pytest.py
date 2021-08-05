from pathlib import Path
import json
import subprocess
import shutil


def have_tests_failed(dir_name):
    """
    Returns:
        int : Based on its value, one of the following situations happened:

            - 0: Tests were successful.
            - 1: Tests failed.
            - 2: pycache directory does not exist or tests were not performed.
    """
    # TODO: robustness still to be confirmed

    pycache_path = _get_pycache_path(dir_name)
    if pycache_path is None:
        return 2

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


def run_tests(dir_name, rm_cache=True):
    """
    Args:
        rm_cache (bool) : Removes pytest_cache previous to tests.
    """
    if rm_cache:
        _rm_pycache(dir_name)

    # try make test
    success = _make_test(dir_name)

    if not success:
        success = _run_pytest(dir_name)

    return success


def _read_info_from_json(filename):
    with open(filename, 'r') as file:
        info = json.load(file)

    return info


def _get_pycache_path(dir_name):
    pycache_paths = list(Path(dir_name).glob('**/.pytest_cache'))
    if len(pycache_paths) == 0:
        return None
    else:
        return pycache_paths[0]


def _rm_pycache(dir_name):
    pycache_path = _get_pycache_path(dir_name)
    if pycache_path is not None:
        shutil.rmtree(pycache_path)


def _make_test(dir_name):
    return _run_cmd(['make', 'test'], dir_name) != ''


def _run_pytest(dir_name):
    # TODO: make more robust with pytest not found?
    stdout = _run_cmd(['pytest'], dir_name)
    return 'no tests ran' not in stdout


def _run_cmd(cmd_ls, dir_name):

    result = subprocess.run(cmd_ls, stdout=subprocess.PIPE,
                            universal_newlines=True, cwd=dir_name)

    return result.stdout
