import os

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


def open_package(package_name, parent_path='.', installed=False,
                 subl_cmd='subl', add=True):

    # get package path
    parent_path, package, _ = get_import_location(
        package_name, parent_path, installed)

    # open
    cmd = f'{subl_cmd} {parent_path / package_name}'
    if add:
        cmd += ' -a'
    os.system(cmd)
    print(f'Added {package} to sublime.')
