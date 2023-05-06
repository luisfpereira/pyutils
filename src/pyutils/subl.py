from pathlib import Path
import subprocess

from pyutils.exceptions import (
    NotFoundError,
    MultipleFoundError,
)
from pyutils.path import (
    find_repo_path,
    ImportStatement,
    get_site_packages_path,
)


class SublimeConfig:
    def __init__(
        self,
        subl_cmd: str = "subl",
        add: bool = True,
    ):
        self.subl_cmd = subl_cmd
        self.add = add

    def run_add_path(self, path: Path):
        cmd = f" {self.subl_cmd} {path}"
        if self.add:
            cmd += " -a"

        _run_cmd(cmd)


def open_code(
    import_: str,
    search_path: Path = None,
    installed: bool = None,
    subl_config: SublimeConfig = None,
):
    import_statement = ImportStatement(import_, installed=installed)

    path = import_statement.find_package_path(search_path=search_path)

    search_path_str = search_path or ""
    if installed or installed is None:
        if search_path_str:
            search_path_str += "or "
        search_path_str += str(get_site_packages_path())

    _check_none_or_multiple(path, import_, search_path_str)

    import_statement.set_path(path)
    if import_statement.is_module and not import_statement.full_path.exists():
        _not_found_error(import_, search_path_str)

    subl_config = subl_config or SublimeConfig()
    subl_config.run_add_path(import_statement.full_path)

    return import_statement


def open_repo(
    repo_name: str,
    search_path: Path = Path("."),
    subl_config: SublimeConfig = None,
):
    path = find_repo_path(search_path, repo_name)

    _check_none_or_multiple(path, repo_name, str(search_path))

    subl_config = subl_config or SublimeConfig()
    subl_config.run_add_path(path)

    return path


def _check_none_or_multiple(path: Path, name: str, search_path_str: str):
    if path is None:
        _not_found_error(name, search_path_str)

    if isinstance(path, list):
        _found_multiple_error(path, name, search_path_str)


def _not_found_error(name: str, search_path_str: str):
    raise NotFoundError(f"Cannot find `{name}` in {search_path_str}.")


def _found_multiple_error(
    paths: list[Path],
    name: str,
    search_path_str: str,
):
    msg = f"More than one `{name}` found in `{search_path_str}`:\n"
    spaces = 4 * " "
    for path in paths:
        msg += f"{spaces}-{str(path)}\n"
    msg += "Be more specific."

    raise MultipleFoundError(msg)


def _run_cmd(cmd):
    sp = subprocess.Popen(["/bin/bash", "-i", "-c", cmd])
    sp.communicate()
