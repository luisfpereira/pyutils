import os
from pathlib import Path

from .utils import get_import_location


def open_module(import_statement, parent_path='.', installed=False,
                subl_cmd='subl', add=True):

    # get module and package
    parent_path, package, module_path = get_import_location(
        import_statement, parent_path, installed)

    # open
    cmd = f'{subl_cmd} {parent_path / package / module_path}.py'
    if add:
        cmd += ' -a'
    os.system(cmd)
