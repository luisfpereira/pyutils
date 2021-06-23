from pathlib import Path

import click

from pyutils.callgraph.pyan import create_callgraph
from pyutils.subl import open_module
from pyutils.subl import open_package
from pyutils.subl import open_repo


@click.command()
@click.argument('import_statement', nargs=1, type=str)
@click.option('--fmt', '-f', nargs=1, type=str, default='svg')
@click.option('--path', '-p', nargs=1, type=str,
              default=Path.home() / 'Repos')
@click.option('--installed', '-i', is_flag=True)
@click.option('--output-path', '-d', type=str,
              default=Path.home() / 'Pictures' / 'Graphs')
@click.option('--output-filename', '-o', type=str, default='myuses')
def make_callgraph(import_statement, fmt, path, installed, output_path,
                   output_filename):
    # TODO: add yml config file
    # TODO: add open_cmd
    # TODO: add graph controls to arg
    # TODO: add help

    create_callgraph(import_statement, fmt=fmt, parent_path=path,
                     installed=installed, output_path=output_path,
                     output_filename=output_filename)


@click.command()
@click.argument('import_statement', nargs=1, type=str)
@click.option('--path', '-p', nargs=1, type=str,
              default=Path.home() / 'Repos')
@click.option('--installed', '-i', is_flag=True)
@click.option('--new-window', '-n', is_flag=True)
def open_module_subl(import_statement, path, installed, new_window):
    open_module(import_statement, path=path, installed=installed,
                add=not new_window)


@click.command()
@click.argument('package_name', nargs=1, type=str)
@click.option('--path', '-p', nargs=1, type=str,
              default=Path.home() / 'Repos')
@click.option('--installed', '-i', is_flag=True)
@click.option('--new-window', '-n', is_flag=True)
def open_package_subl(package_name, path, installed, new_window):
    open_package(package_name, path=path, installed=installed,
                 add=not new_window)


@click.command()
@click.argument('repo_name', nargs=1, type=str)
@click.option('--path', '-p', nargs=1, type=str,
              default=Path.home() / 'Repos')
@click.option('--new-window', '-n', is_flag=True)
def open_repo_subl(repo_name, path, new_window):
    open_repo(repo_name, path=path, add=not new_window)


@click.command()
@click.argument('filename', nargs=1, type=str)
@click.option('--full-name', '-f', is_flag=True)
@click.option('--add-types', '-t', is_flag=True)
def show_hdf_tree(filename, full_name, add_types):
    import h5py
    from pyutils.hdf import get_hdf_tree
    from pyutils.viz_tree import print_tree

    file = h5py.File(filename, 'r')

    root = get_hdf_tree(file, simplify_names=not full_name, append_type=add_types)
    print_tree(root)

    file.close()


@click.command()
def codecog_eq():
    import pyperclip
    from pyutils.codecogs import get_image_url

    equation = rf'{pyperclip.paste()}'
    print(f'Read equation: {equation}')

    url = get_image_url(equation)
    print(f'URL (copied to clipboard): {url}')
    pyperclip.copy(url)
