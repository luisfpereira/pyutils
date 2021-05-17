from pathlib import Path
import site


def find_package_parent_path(path, package_name):

    # get all packages and subpackages
    filenames = [path_.parent for path_ in path.glob('**/__init__.py')
                 if path_.parent.name == package_name]

    # only one possibility
    if len(filenames) == 1:
        return filenames[0].parent

    # in case a subpackage is found
    for filename in filenames:
        if len([path_ for path_ in filename.parent.glob('__init__.py')]) == 0:
            return filename.parent

    return None


def get_site_packages_path():
    return Path(site.getsitepackages[0])


def get_package_name_from_import(import_str):
    return import_str.split('.')[0]


def get_module_name_from_import(import_str):
    return '.'.join(import_str.split('.')[1:])


def get_valid_path_from_import(import_str):
    return Path(*import_str.split('.'))


def get_import_location(import_statement, parent_path='.', installed=False):

    package = get_package_name_from_import(import_statement)
    module = get_module_name_from_import(import_statement)

    # get module and package paths
    if installed:
        parent_path = get_site_packages_path()
    else:
        parent_path = find_package_parent_path(parent_path, package)
    if parent_path is None:
        raise Exception(f'{package} was not found.')
    else:
        print(f'Found {package} in {parent_path}.')
    module_path = get_valid_path_from_import(module)

    return parent_path, package, module_path
