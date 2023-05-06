from pathlib import Path
import site
import warnings


def convert_dirname_to_path(dir_name):
    """
    Notes:
        Handles definition of home with `~`.
    """
    # TODO: check need
    dir_name_ls = dir_name.split("/")
    if dir_name_ls[0] == "~":
        path = Path.home() / "/".join(dir_name_ls[1:])
    else:
        path = Path(dir_name)

    return path


def find_package_path(
    search_path: Path,
    package_name: str,
    exclude_patterns: tuple[str] = ("build/lib",),
):

    # get all packages and subpackages
    dir_paths = [
        path_.parent
        for path_ in search_path.glob("**/__init__.py")
        if path_.parent.name == package_name
    ]

    # remove subpackages
    dir_paths = filter(
        lambda path: (path.parent / "__init__.py").exists() == 0, dir_paths
    )

    # exclude patterns
    dir_paths = [
        dir_path
        for dir_path in dir_paths
        if not exclude_path_patterns(dir_path, exclude_patterns)
    ]

    if len(dir_paths) == 1:
        return dir_paths[0]

    if len(dir_paths) > 1:
        return dir_paths

    return None


def exclude_path_patterns(path: Path, exclude_patterns: tuple[str]):
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


class ImportStatement:
    """A nice way to find info related with an import statement.

    Considers only package, subpackage, or module.
    """

    def __init__(
        self,
        import_: str,
        installed: bool = None,
    ):
        self.import_ = import_
        self.installed = installed

        self.path = None

    def set_path(self, path):
        self.path = path
        return self

    @property
    def package_name(self):
        return self.import_.split(".")[0]

    @property
    def module_name(self):
        if not self.is_module:
            return self.package_name

        return ".".join(self.import_.split(".")[1:])

    def is_module(self):
        return "." not in self.import_

    @property
    def full_path(self):
        if not self.is_module:
            return self.path

        import_ls = self.import_.split(".")[1:]
        import_ls[-1] = import_ls[-1] + ".py"
        return self.path / Path(*import_ls)

    def find_package_path(self, search_path: Path = None):
        package_name = self.package_name
        if self.installed is None:
            parent_path = find_package_path(search_path, package_name)
            if parent_path is None:
                parent_path = find_package_path(
                    get_site_packages_path(),
                    self.package_path,
                )

        else:
            if self.installed:
                if search_path is not None:
                    warnings.warn("`search_path` ignored.")
                search_path = get_site_packages_path()

            parent_path = find_package_path(search_path, self.package_name)

        return parent_path


def find_repo_path(
    search_path: Path,
    repo_name: str,
):
    """Recursively searchs for repo path."""
    filenames = [
        path_.parent
        for path_ in search_path.glob("**/.git")
        if path_.parent.name == repo_name
    ]

    if len(filenames) == 1:
        return filenames[0]

    if len(filenames) > 1:
        return filenames

    return None


def find_all_repos_paths(path, sort=True):
    # TODO: rename
    paths = [path.parent for path in path.glob("**/.git")]
    if sort:
        paths = sorted(paths, key=lambda x: x.name.lower())

    return paths
