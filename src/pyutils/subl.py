from pathlib import Path
import subprocess

from pyutils.path import get_import_location
from pyutils.path import find_repo_parent_path


def open_module(import_statement, path=".", installed=False, subl_cmd="subl", add=True):

    # get module and package
    parent_path, package, module_path = get_import_location(
        import_statement, path, installed, verbose=True
    )

    # open
    cmd = f"{subl_cmd} {parent_path / package / module_path}.py"
    if add:
        cmd += " -a"

    _run_cmd(cmd)


def open_package(package_name, path=".", installed=False, subl_cmd="subl", add=True):

    # get package path
    parent_path, package, _ = get_import_location(
        package_name, path, installed, verbose=True
    )

    # open
    cmd = f"{subl_cmd} {parent_path / package_name}"
    if add:
        cmd += " -a"

    _run_cmd(cmd)

    print(f"added {package} to sublime.")


def open_repo(repo_name, path=".", subl_cmd="subl", add=True):
    parent_path = find_repo_parent_path(Path(path), repo_name)

    # open
    cmd = f" {subl_cmd} {parent_path / repo_name}"
    if add:
        cmd += " -a"

    _run_cmd(cmd)

    print(f"Added {repo_name} to sublime.")


def _run_cmd(cmd):
    sp = subprocess.Popen(["/bin/bash", "-i", "-c", cmd])
    sp.communicate()
