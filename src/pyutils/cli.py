from pathlib import Path

import click

# TODO: move to the interior of the functions
from pyutils.callgraph.pyan import create_callgraph
from pyutils.subl import open_module
from pyutils.subl import open_package
from pyutils.subl import open_repo

CHECKOUT_MSGS = {
    0: 'Successfully checked out.',
    1: 'Failed: dirty repo.',
    2: 'Failed: inexistent branch.',
}


PULL_MSGS = {
    0: 'Successfully pulled changes.',
    1: 'No changes.',
    2: 'Failed: no upstream.',
    3: 'Failed: merge_conflicts.',
    4: 'Failed: local non-commited changes.'
}

UNKNOWN_ERROR_MSG = 'Failed: unknown error.'


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
    repos_dict = _get_git_repos(dirname, ignore)

    for repo_name, repo in repos_dict.items():
        active_branch = repo.active_branch
        print(f'{repo_name}: {active_branch.name}')


@click.command()
@click.argument('repo_name', nargs=1, type=str)
@click.option('--dirname', '-d', type=str, default='~/Repos/')
@click.option('--origin', '-o', is_flag=True)
def print_repo_branches(repo_name, dirname, origin):
    """Prints repo branches (active in first place).
    """
    from pyutils.git import get_repo_branch_names

    repo = _get_git_repo(dirname, repo_name)

    branch_names = get_repo_branch_names(repo, include_origin=origin,
                                         active_first=True)

    for branch_name in branch_names:
        print(f'{branch_name}')


@click.command()
@click.option('--dirname', '-d', type=str, default='~/Repos')
@click.option('--ignore', '-i', is_flag=True)
@click.option('--origin', '-o', is_flag=True)
def print_repos_branches(dirname, ignore, origin):
    from pyutils.git import get_repo_branch_names

    repos_dict = _get_git_repos(dirname, ignore)

    for repo_name, repo in repos_dict.items():
        print(f'{repo_name}')
        branch_names = get_repo_branch_names(repo, include_origin=origin)
        for branch_name in branch_names:
            print(f'  {branch_name}')


@click.command()
@click.option('--dirname', '-d', type=str, default='~/Repos')
@click.option('--ignore', '-i', is_flag=True)
@click.option('--untracked', '-u', is_flag=True)
def print_repos_dirty(dirname, ignore, untracked):
    repos_dict = _get_git_repos(dirname, ignore)

    dirty_repos_names = [repo_name for repo_name, repo in repos_dict.items()
                         if repo.is_dirty(untracked_files=untracked)]
    print('\n'.join(dirty_repos_names))


@click.command()
@click.argument('repo_name', nargs=1, type=str)
@click.argument('branch_name', nargs=1, type=str)
@click.option('--dirname', '-d', type=str, default='~/Repos')
@click.option('--force', '-f', is_flag=True)
def checkout_repo(repo_name, branch_name, dirname, force):
    from pyutils.git import checkout

    repo = _get_git_repo(dirname, repo_name)
    var_checkout = checkout(repo, branch_name, force=force)
    msg = CHECKOUT_MSGS.get(var_checkout, UNKNOWN_ERROR_MSG)
    print(msg)


@click.command()
@click.option('--dirname', '-d', type=str, default='~/Repos')
def checkout_repos(dirname):
    from pyutils.git import checkout

    repos_info = _get_repos_checkout_info_from_file(dirname)
    for repo_name, info in repos_info.items():
        print(f'{repo_name}')
        print(info)

        var_checkout = checkout(info['repo'], info['branch_name'],
                                force=info['force_checkout'])
        msg = CHECKOUT_MSGS.get(var_checkout, UNKNOWN_ERROR_MSG)
        print(f'  {msg}')


@click.command()
@click.argument('repo_name', nargs=1, type=str)
@click.option('--dirname', '-d', type=str, default='~/Repos')
def pull_repo(repo_name, dirname):
    from pyutils.git import pull

    repo = _get_git_repo(dirname, repo_name)
    var_pull = pull(repo)

    msg = PULL_MSGS.get(var_pull, UNKNOWN_ERROR_MSG)
    print(msg)


@click.command()
@click.option('--dirname', '-d', type=str, default='~/Repos')
@click.option('--ignore', '-i', is_flag=True)
def pull_repos(dirname, ignore):
    from pyutils.git import pull

    repos_dict = _get_git_repos(dirname, ignore)

    # pull repos
    msgs = {key: [] for key in PULL_MSGS.keys()}
    unknown = []
    for repo_name, repo in repos_dict.items():
        var_pull = pull(repo)
        msgs.get(var_pull, unknown).append(repo_name)

    # print messages expected behavior
    for msg_val, repos_names in msgs.items():
        if len(repos_names) > 0:
            print(PULL_MSGS[msg_val])
            print('  ' + '\n  '.join(repos_names))

    # print unknown errors
    if len(unknown) > 0:
        print(UNKNOWN_ERROR_MSG)
        print('  ' + '\n  '.join(unknown))


@click.command()
@click.option('--dirname', '-d', type=str, default='~/Repos')
@click.option('--ignore', '-i', is_flag=True)
def print_repos_no_upstream(dirname, ignore):
    """Prints active branches with no upstreams.

    Notes:
        Active branches with no upstreams cannot be pulled.
    """
    from pyutils.git import has_upstream

    repos_dict = _get_git_repos(dirname, ignore)
    no_upstream_names = {repo_name for repo_name, repo in repos_dict.items()
                         if not has_upstream(repo)}

    print('\n'.join(no_upstream_names))


def _read_git_repos_file(parse=True):
    from pyutils import get_home_path

    file_path = get_home_path() / 'git_repos.txt'
    with open(file_path, 'r') as file:
        repos_txt = file.read()

    if parse:
        return _parse_git_repos_file(repos_txt)
    else:
        return repos_txt


def _parse_git_repos_file(repos_txt):
    lines = [repo_name.strip() for repo_name in repos_txt.split('\n') if repo_name[0] != '#']

    info = {}
    for line in lines:
        line_split = [name.strip() for name in line.split(',')]
        repo_name = line_split[0]
        branch_name = line_split[1] if len(line_split) > 1 else None
        force_checkout = _transform_bool(line_split[2]) if len(line_split) > 2 else False

        info[repo_name] = {
            'branch_name': branch_name,
            'force_checkout': force_checkout
        }

    return info


def _get_repos_names_from_file():
    info = _read_git_repos_file(parse=True)

    return list(info.keys())


def _get_repos_checkout_info_from_file(dirname):
    repos_info = _read_git_repos_file(parse=True)

    new_repos_info = {}
    for repo_name, info in repos_info.items():
        if info['branch_name'] is not None:
            new_repos_info[repo_name] = info
            new_repos_info[repo_name]['repo'] = _get_git_repo(dirname, repo_name)

    return new_repos_info


def _get_git_repo(dirname, repo_name):
    from pyutils.path import convert_dirname_to_path
    from pyutils.git import get_repo

    path = convert_dirname_to_path(dirname)
    repo = get_repo(repo_name, path=path)

    return repo


def _get_git_repos(dirname, ignore):
    """Get repos from directory (all or from file).

    Notes:
        Use flag `ignore` to ignore file and show all the repos in a path.

        If `ignore` is False, then dirname tells were to look for the repo.
    """
    from pyutils.path import convert_dirname_to_path
    from pyutils.git import get_repos_from_path
    from pyutils.git import get_repo

    path = convert_dirname_to_path(dirname)

    if ignore:
        repos_dict = get_repos_from_path(path)
    else:
        # TODO: add not found
        repos_names = _get_repos_names_from_file()
        repos_dict = {name: get_repo(name, path=path) for name in repos_names}

    return repos_dict


def _transform_bool(string):
    if string.lower() == 'false':
        return False
    elif string.lower() == 'true':
        return True
