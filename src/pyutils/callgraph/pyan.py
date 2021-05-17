import os
from pathlib import Path

from ..utils import get_import_location


def create_callgraph(import_statement, fmt='svg',
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
    parent_path, package, module_path = get_import_location(
        import_statement, parent_path, installed)

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
