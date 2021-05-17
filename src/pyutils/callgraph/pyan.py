import os
from pathlib import Path

from ..utils import find_package_parent_path
from ..utils import get_package_name_from_import
from ..utils import get_module_name_from_import
from ..utils import get_valid_path_from_import
from ..utils import get_site_packages_path


def create_callgraph(import_str, fmt='svg',
                     parent_path=None, installed=False, output_path=None,
                     output_filename='myuses', open_cmd=None,
                     graph_controls=('uses', 'no-defines', 'colored', 'grouped')):

    # initialization
    if parent_path is None:
        parent_path = Path.home() / 'Repos'

    if output_path is None:
        output_path = Path.home() / 'Pictures' / 'Graphs'

    output_filename = output_path / f'{output_filename}.{fmt}'

    # get module and package
    package = get_package_name_from_import(import_str)
    module = get_module_name_from_import(import_str)

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

    # launch pyan
    cmd = (
        f'pyan3 {parent_path / package / module_path}.py '
        f'--{" --".join(graph_controls)} '
        f'--{fmt} --root {parent_path / package} > {output_filename}'
    )
    os.system(cmd)
    print(f'Created file {output_filename}.')

    # open file
    if open_cmd:
        os.system(f'{open_cmd} {output_filename}')
