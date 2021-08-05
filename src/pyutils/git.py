from pathlib import Path

from git import Repo
from git.exc import GitCommandError

from pyutils.path import find_repo_path
from pyutils.path import find_all_repos_paths

# TODO: remove local changes?


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


def get_repo_branch_names(repo, include_origin=False, active_first=True):
    branch_names = [head.name for head in repo.heads]
    if include_origin:
        branch_names.extend([ref.name for ref in repo.remotes.origin.refs])

    if active_first:
        active_branch_name = repo.active_branch.name
        branch_names.remove(active_branch_name)
        branch_names.insert(0, active_branch_name)

    return branch_names


def get_head(repo, branch_name):
    head = None
    for head in repo.heads:
        if head.name == branch_name:
            return head

    return None


def checkout(repo, branch_name, force=False):
    """Checks out to existing branch.

    Returns:
        int : Based on its value, one of the following situations happened:

            - 0: Success.
            - 1: Failed: dirty repo.
            - 2: Failed: branch name does does exist.
            - GitCommandError: Failed: unknown error origin.
    """

    # verify if already in the right branch
    if repo.active_branch.name == branch_name:
        return 0

    # verify if it is dirty
    if repo.is_dirty(untracked_files=False) and not force:
        return 1

    # find head
    head = get_head(repo, branch_name)
    if head is None:
        return 2

    # checkout
    try:
        head.checkout(force=force)
        return 0
    except GitCommandError as e:
        return e


def pull(repo):
    """Pulls current active branch.

    Returns:
        int or GitCommandError: Based on its value, one of the following
        situations happened:

            - 0: Success: changes.
            - 1: Success: no changes.
            - 2: Failed: no upstream.
            - 3: Failed: merge conflicts (merge is aborted).
            - 4: Failed: conflict with local non-commited changes.
            - GitCommandError: Failed: unknown error origin.
    """
    up_to_date_var = is_up_to_date(repo)  # anaconda does not allow walrus
    if up_to_date_var:
        return up_to_date_var  # existence of upstream is also verified

    try:
        repo.remotes.origin.pull()
        return 0

    except GitCommandError as e:
        msg_local_conflict = "stderr: 'error: Your local changes to the following files would be overwritten by merge:'"

        stderr = e.stderr
        if stderr == '':
            repo.git.execute(['git', 'merge', '--abort'])
            return 3
        elif stderr.strip() == msg_local_conflict:
            return 4
        else:
            return e


def is_up_to_date(repo):
    """Checks if current active branch is up-to-date.

    Returns:
        int : Based on its value, one of the following situations happened:

            - 0: Is outdated: last commit in the origin is
            - 1: Is up-to-date.
            - 2: No upstream.
    """
    if not has_upstream(repo):
        return 2

    repo.git.fetch()

    local = repo.head.commit
    remote = repo.active_branch.tracking_branch().commit
    if local == remote:
        return 1
    else:
        return 0


def has_upstream(repo):
    """Checks if activate branch has upstream.
    """
    return repo.active_branch.tracking_branch() is not None
