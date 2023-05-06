from pathlib import Path
import site


def convert_dirname_to_path(dir_name):
    """
    Notes:
        Handles definition of home with `~`.
    """
    dir_name_ls = dir_name.split("/")
    if dir_name_ls[0] == "~":
        path = Path.home() / "/".join(dir_name_ls[1:])
    else:
        path = Path(dir_name)

    return path


def find_package_parent_path(path, package_name, exclude_patterns=("build/lib",)):

    # get all packages and subpackages
    dir_paths = [
        path_.parent
        for path_ in Path(path).glob("**/__init__.py")
        if path_.parent.name == package_name
    ]

    # exclude patterns
    dir_paths = [
        dir_path
        for dir_path in dir_paths
        if not exclude_path_patterns(dir_path, exclude_patterns)
    ]

    # only one possibility
    if len(dir_paths) == 1:
        return dir_paths[0].parent

    # in case a subpackage is found
    for dir_path in dir_paths:

        if len([path_ for path_ in dir_path.parent.glob("__init__.py")]) == 0:
            return dir_path.parent

    return None


def exclude_path_patterns(path, exclude_patterns):
    """
    Args:
        exclude_patterns (array-like): patterns to be ignored.
            Relative to found folders, i.e. if folder to ignore is
            'build/lib/package_name', then pass 'build/lib'.
    """
    for exclude_pattern in exclude_patterns:
        path_ = path.parent
        for name in reversed(exclude_pattern.split("/")):
            if name != path_.name:
                break
            path_ = path_.parent
        else:
            return True

    return False


def get_site_packages_path():
    return Path(site.getsitepackages()[0])


def get_package_name_from_import(import_str):
    return import_str.split(".")[0]


def get_module_name_from_import(import_str):
    return ".".join(import_str.split(".")[1:])


def get_valid_path_from_import(import_str):
    return Path(*import_str.split("."))


def get_import_location(import_statement, path=".", installed=False, verbose=False):

    package = get_package_name_from_import(import_statement)
    module = get_module_name_from_import(import_statement)

    # get module and package paths
    if installed:
        parent_path = get_site_packages_path()
    else:
        parent_path = find_package_parent_path(path, package)

    if parent_path is None:
        raise Exception(f"{package} was not found.")
    elif verbose:
        print(f"Found {package} in {parent_path}.")

    module_path = get_valid_path_from_import(module)

    return parent_path, package, module_path


def find_repo_parent_path(path, repo_name):

    # get all packages and subpackages
    filenames = [
        path_.parent for path_ in path.glob("**/.git") if path_.parent.name == repo_name
    ]

    # only one possibility
    if len(filenames) == 1:
        return filenames[0].parent
    elif len(filenames) > 1:
        raise Exception("More than one repo with the given name.")
    else:
        raise Exception("Repo was not found.")

    return None


def find_repo_path(path, repo_name):
    return find_repo_parent_path(path, repo_name) / repo_name


def find_all_repos_paths(path, sort=True):
    paths = [path.parent for path in path.glob("**/.git")]
    if sort:
        paths = sorted(paths, key=lambda x: x.name.lower())

    return paths
