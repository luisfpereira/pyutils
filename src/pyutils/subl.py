import os
from pathlib import Path

from .utils import get_import_location
from .utils import find_repo_parent_path


def open_module(import_statement, path='.', installed=False,
                subl_cmd='subl', add=True):

    # get module and package
    parent_path, package, module_path = get_import_location(
        import_statement, path, installed)

    # open
    cmd = f'{subl_cmd} {parent_path / package / module_path}.py'
    if add:
        cmd += ' -a'
    os.system(cmd)


def open_package(package_name, path='.', installed=False,
                 subl_cmd='subl', add=True):

    # get package path
    parent_path, package, _ = get_import_location(
        package_name, path, installed)

    # open
    cmd = f'{subl_cmd} {parent_path / package_name}'
    if add:
        cmd += ' -a'
    os.system(cmd)
    print(f'Added {package} to sublime.')


def open_repo(repo_name, path='.', subl_cmd='subl', add=True):
    parent_path = find_repo_parent_path(Path(path), repo_name)

    # open
    cmd = f'{subl_cmd} {parent_path / repo_name}'
    if add:
        cmd += ' -a'
    os.system(cmd)
    print(f'Added {repo_name} to sublime.')
