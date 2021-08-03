from pathlib import Path

import click

# TODO: move to the interior of the functions
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


@click.command()
@click.argument('filename', nargs=1, type=str)
@click.option('--fmt', '-f', nargs=1, type=str, default='svg')
@click.option('--outputs-dir', '-o', nargs=1, type=str, default='outputs')
def my_dot(filename, fmt, outputs_dir):
    from pyutils.graphviz import export_graph
    export_graph(filename, fmt=fmt, outputs_dir=outputs_dir)


@click.command()
@click.option('--inputs-dir', '-i', type=str, default='.')
@click.option('--fmt', '-f', nargs=1, type=str, default='svg')
@click.option('--outputs-dir', '-o', nargs=1, type=str, default='outputs')
def my_dot_all(inputs_dir, fmt, outputs_dir):
    import glob
    from pyutils.graphviz import export_graph

    for filename in glob.glob(f'{inputs_dir}/*.gv'):
        export_graph(filename, fmt=fmt, outputs_dir=outputs_dir)


@click.command()
@click.option('--dirname', '-d', type=str, default='~/Repos')
@click.option('--ignore', '-i', is_flag=True)
def print_repos_active_branch(dirname, ignore):
    from pyutils.git import get_repo_active_branch

    repos_dict = _get_git_repos(dirname, ignore)

    for repo_name, repo in repos_dict.items():
        active_branch = get_repo_active_branch(repo)
        print(f'{repo_name}: {active_branch.name}')


@click.command()
@click.argument('repo_name', nargs=1, type=str)
@click.option('--dirname', '-d', type=str, default='~/Repos/')
def print_repo_branches(repo_name, dirname):
    from pyutils.path import convert_dirname_to_path
    from pyutils.git import get_repo
    from pyutils.git import get_repo_branch_names

    path = convert_dirname_to_path(dirname)
    repo = get_repo(repo_name, path=path)
    branch_names = get_repo_branch_names(repo)

    for branch_name in branch_names:
        print(f'{branch_name}')


@click.command()
@click.option('--dirname', '-d', type=str, default='~/Repos')
@click.option('--ignore', '-i', is_flag=True)
def print_repos_branches(dirname, ignore):
    from pyutils.git import get_repo_branch_names

    repos_dict = _get_git_repos(dirname, ignore)

    for repo_name, repo in repos_dict.items():
        print(f'{repo_name}')
        branch_names = get_repo_branch_names(repo)
        for branch_name in branch_names:
            print(f'  {branch_name}')


def _read_git_repos_file():
    from pyutils import get_home

    file_path = get_home() / 'git_repos.txt'
    with open(file_path, 'r') as file:
        repos_txt = file.read()

    return [repo_name.strip() for repo_name in repos_txt.split()]


def _get_git_repos(dirname, ignore):
    """Get repos from directory (all or from file).

    Notes:
        Use flag `ignore` to ignore file and show all the repos in a path.

    """
    from pyutils.path import convert_dirname_to_path
    from pyutils.git import get_repos_from_path
    from pyutils.git import get_repo

    path = convert_dirname_to_path(dirname)

    if ignore:
        repos_dict = get_repos_from_path(path)
    else:
        repos_names = _read_git_repos_file()
        repos_dict = {name: get_repo(name, path=path) for name in repos_names}

    return repos_dict
