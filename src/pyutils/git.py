from pathlib import Path

from git import Repo
from git.exc import GitCommandError

from pyutils.path import find_repo_path
from pyutils.path import find_all_repos_paths

# TODO: check current branches (of a path - cerfacs or git as default - or of a list of repos in a txt)
# TODO: fetch all branches
# TODO: checkout to specific branches (need to deal with error if local changes -> success vs failed)
# TODO: launch tests in all related packages
# TODO: repo origin branches


def get_repo(repo_name, path=Path.home() / 'Repos'):
    repo_path = find_repo_path(path, repo_name)
    return get_repo_from_path(repo_path)


def get_repo_from_path(repo_path):
    return Repo(repo_path)


def get_repos_from_path(path):
    repos_paths = find_all_repos_paths(path)
    return get_repos_from_paths(repos_paths)


def get_repos_from_paths(repos_paths):
    repos = {}
    for repo_path in repos_paths:
        repo = get_repo_from_path(repo_path)
        name = get_repo_name(repo)

        repos[name] = repo

    return repos


def get_repo_name(repo):
    return repo.git_dir.split('/')[-2]


def get_repo_branch_names(repo):
    # TODO: add include origin
    return [head.name for head in repo.heads]


def get_repo_active_branch(repo):
    return repo.active_branch


def checkout(repo, branch_name, force=False):
    """Checkouts to existing branch.

    Returns:
        int : Based on its value, one of the following situations happen:

            - 0: success
            - 1: branch name does does exist
            - 2: changes in current tree does not allow checkout
    """

    # find head
    head = None
    for head in repo.heads:
        if head.name == branch_name:
            break
    else:
        return 1

    # checkout
    try:
        head.checkout(force=force)
        return 0
    except GitCommandError:
        return 2
