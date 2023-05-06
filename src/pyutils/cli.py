from pathlib import Path
import json

import click

# TODO: print packages that need push/pull

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
    from pyutils.callgraph.pyan import create_callgraph
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
    from pyutils.subl import open_module
    open_module(import_statement, path=path, installed=installed,
                add=not new_window)


@click.command()
@click.argument('package_name', nargs=1, type=str)
@click.option('--path', '-p', nargs=1, type=str,
              default=Path.home() / 'Repos')
@click.option('--installed', '-i', is_flag=True)
@click.option('--new-window', '-n', is_flag=True)
def open_package_subl(package_name, path, installed, new_window):
    from pyutils.subl import open_package
    open_package(package_name, path=path, installed=installed,
                 add=not new_window)


@click.command()
@click.argument('repo_name', nargs=1, type=str)
@click.option('--path', '-p', nargs=1, type=str,
              default=Path.home() / 'Repos')
@click.option('--new-window', '-n', is_flag=True)
def open_repo_subl(repo_name, path, new_window):
    from pyutils.subl import open_repo
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
@click.option('--outputs-dir', '-o', nargs=1, type=str, default='_outputs')
def my_dot(filename, fmt, outputs_dir):
    from pyutils.graphviz import export_graph
    export_graph(filename, fmt=fmt, outputs_dir=outputs_dir)


@click.command()
@click.option('--inputs-dir', '-i', type=str, default='.')
@click.option('--fmt', '-f', nargs=1, type=str, default='svg')
@click.option('--outputs-dir', '-o', nargs=1, type=str, default='_outputs')
def my_dot_all(inputs_dir, fmt, outputs_dir):
    import glob
    from pyutils.graphviz import export_graph

    for ext in ['dot', 'gv']:
        for filename in glob.glob(f'{inputs_dir}/*.{ext}'):
            export_graph(filename, fmt=fmt, outputs_dir=outputs_dir)


@click.command()
@click.option('--search-dirname', '-s', type=str, default='~/Repos')
@click.option('--dirname', '-d', type=str, default=None)
def print_repos_active_branch(search_dirname, dirname):
    repos_dict = _get_git_repos(search_dirname, dirname)

    for repo_name, repo in repos_dict.items():
        active_branch = repo.active_branch
        print(f'{repo_name}: {active_branch.name}')


@click.command()
@click.argument('repo_name', nargs=1, type=str)
@click.option('--search-dirname', '-s', type=str, default='~/Repos/')
@click.option('--origin', '-o', is_flag=True)
def print_repo_branches(repo_name, search_dirname, origin):
    """Prints repo branches (active in first place).
    """
    from pyutils.git import get_repo_branch_names

    repo = _get_git_repo(search_dirname, repo_name)

    branch_names = get_repo_branch_names(repo, include_origin=origin,
                                         active_first=True)

    for branch_name in branch_names:
        print(f'{branch_name}')


@click.command()
@click.option('--search-dirname', '-s', type=str, default='~/Repos')
@click.option('--dirname', '-d', type=str, default=None)
@click.option('--origin', '-o', is_flag=True)
def print_repos_branches(search_dirname, dirname, origin):
    from pyutils.git import get_repo_branch_names

    repos_dict = _get_git_repos(search_dirname, dirname)

    for repo_name, repo in repos_dict.items():
        print(f'{repo_name}')
        branch_names = get_repo_branch_names(repo, include_origin=origin)
        for branch_name in branch_names:
            print(f'  {branch_name}')


@click.command()
@click.option('--search-dirname', '-s', type=str, default='~/Repos')
@click.option('--dirname', '-d', type=str, default=None)
@click.option('--untracked', '-u', is_flag=True)
def print_repos_dirty(search_dirname, dirname, untracked):
    repos_dict = _get_git_repos(search_dirname, dirname)

    dirty_repos_names = [repo_name for repo_name, repo in repos_dict.items()
                         if repo.is_dirty(untracked_files=untracked)]
    print('\n'.join(dirty_repos_names))


@click.command()
@click.argument('repo_name', nargs=1, type=str)
@click.argument('branch_name', nargs=1, type=str)
@click.option('--search-dirname', '-s', type=str, default='~/Repos')
@click.option('--force', '-f', is_flag=True)
def checkout_repo(repo_name, branch_name, search_dirname, force):
    from pyutils.git import checkout

    repo = _get_git_repo(search_dirname, repo_name)
    var_checkout = checkout(repo, branch_name, force=force)
    msg = CHECKOUT_MSGS.get(var_checkout, UNKNOWN_ERROR_MSG)
    print(msg)


@click.command()
@click.option('--search-dirname', '-s', type=str, default='~/Repos')
def checkout_repos(search_dirname):
    from pyutils.git import checkout

    repos_info = _get_repos_checkout_info_from_file(search_dirname)
    for repo_name, info in repos_info.items():
        branch_name = info['branch_name']
        print(f'{repo_name} -> {branch_name}')

        var_checkout = checkout(info['repo'], branch_name,
                                force=info['force_checkout'])
        msg = CHECKOUT_MSGS.get(var_checkout, UNKNOWN_ERROR_MSG)
        print(f'  {msg}')


@click.command()
@click.argument('repo_name', nargs=1, type=str)
@click.option('--search-dirname', '-s', type=str, default='~/Repos')
def pull_repo(repo_name, search_dirname):
    from pyutils.git import pull

    repo = _get_git_repo(search_dirname, repo_name)
    var_pull = pull(repo)

    msg = PULL_MSGS.get(var_pull, UNKNOWN_ERROR_MSG)
    print(msg)


@click.command()
@click.option('--search-dirname', '-s', type=str, default='~/Repos')
@click.option('--dirname', '-d', type=str, default=None)
def pull_repos(search_dirname, dirname):
    from pyutils.git import pull
    # TODO: add progress bar

    repos_dict = _get_git_repos(search_dirname, dirname)

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
@click.option('--search-dirname', '-s', type=str, default='~/Repos')
@click.option('--dirname', '-d', type=str, default=None)
def print_repos_no_upstream(search_dirname, dirname):
    """Prints active branches with no upstreams.

    Notes:
        Active branches with no upstreams cannot be pulled.
    """
    from pyutils.git import has_upstream

    repos_dict = _get_git_repos(search_dirname, dirname)
    no_upstream_names = {repo_name for repo_name, repo in repos_dict.items()
                         if not has_upstream(repo)}

    print('\n'.join(no_upstream_names))


@click.command()
@click.option('--project-name', '-p', type=str, default=None)
@click.option('--search-dirname', '-s', type=str, default='~/Repos')
def make_integrated_tests(project_name, search_dirname):
    """
    Notes:
        Assumes Makefile with `make test` exist or `pytest` can be used.
    """
    from pyutils import get_home_path
    from pyutils.git import checkout
    from pyutils.pytest import have_tests_failed
    from pyutils.pytest import run_tests

    # get repos info
    file_path = get_home_path() / 'integrated_tests.json'
    with open(file_path, 'r') as file:
        dict_tests = json.load(file)
    if project_name is None:
        project_name = list(dict_tests.keys())[0]
    repos_info = dict_tests[project_name]

    # get repos
    for repo_name, repo_info in repos_info.items():
        repo = _get_git_repo(search_dirname, repo_name)
        repo_info.append(repo)

    # checkout
    ignore_repos = {}
    only_checkout_repos = {}
    for repo_name, repo_info in repos_info.items():
        branch_name, to_test, repo = repo_info
        var_checkout = checkout(repo, branch_name, force=False)

        if var_checkout != 0:
            ignore_repos[repo_name] = var_checkout
        elif not to_test:
            only_checkout_repos[repo_name] = branch_name

    # make test
    ignore_repos_names = list(ignore_repos.keys()) + list(only_checkout_repos.keys())
    info_test = {0: [], 1: [], 2: []}
    for repo_name, repo_info in repos_info.items():
        if repo_name in ignore_repos_names:
            continue
        repo = repo_info[-1]
        var_run = run_tests(repo.working_dir)
        if not var_run:
            info_test[2].append(repo_name)
            continue

        var_test = have_tests_failed(repo.working_dir)
        info_test[var_test].append(repo_name)

    # print quick summary
    print('\n\nQuick summary\n=============')

    if len(only_checkout_repos) > 0:
        print('\nSuccessfully checked out (only):')
        for repo_name, branch_name in only_checkout_repos.items():
            print(f'  {repo_name} -> {branch_name}')

    if len(ignore_repos) > 0:
        print('\nRepos that failed checkout:')
        for repo_name, error_info in ignore_repos.items():
            print(f'  {repo_name}: {CHECKOUT_MSGS.get(error_info, UNKNOWN_ERROR_MSG)}')

    for val_test, msg in enumerate(['succeeded', 'failed', "didn't run"]):
        if len(info_test[val_test]) > 0:
            print(f'\nRepos that {msg} tests:')
            print('  ' + '\n  '.join(info_test[val_test]))


@click.command()
@click.argument('filename', nargs=1, type=str)
@click.argument('new_basename', nargs=1, type=str)
def rename_hdf_cli(filename, new_basename):
    from pyutils.hdf import rename_hdf

    rename_hdf(filename, new_basename)


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


def _get_git_repos(search_dirname, dirname):
    """Get repos from directory (all or from file).

    Notes:
        If `dirname` is not None, then `search_dirname` is ignored.

        If `dirname` is None, then the file at home is used.
    """
    from pyutils.path import convert_dirname_to_path
    from pyutils.git import get_repos_from_path
    from pyutils.git import get_repo

    if dirname is not None:
        path = convert_dirname_to_path(dirname)
        repos_dict = get_repos_from_path(path)
    else:
        path = convert_dirname_to_path(search_dirname)

        # TODO: add not found
        repos_names = _get_repos_names_from_file()
        repos_dict = {name: get_repo(name, path=path) for name in repos_names}

    return repos_dict


def _transform_bool(string):
    if string.lower() == 'false':
        return False
    elif string.lower() == 'true':
        return True
