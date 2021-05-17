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
