import sys
from pathlib import Path


import typer
from typing_extensions import Annotated

from pyutils.exceptions import (
    NotFoundError,
    MultipleFoundError,
)
from pyutils.subl import open_repo, SublimeConfig, open_code


app = typer.Typer()


@app.command()
def main(
    name: Annotated[str, typer.Argument(help="Repo/package name or module import")],
    search_path: Annotated[Path, typer.Option("--search-path", "-p")] = Path.home()
    / "Repos",
    new_window: Annotated[bool, typer.Option("--new-window", "-n")] = False,
    code: Annotated[
        bool, typer.Option("--code", "-c", help="Search for package or module")
    ] = False,
    installed: Annotated[
        bool, typer.Option("--installed", "-i", help="Search in site packages.")
    ] = False,
):
    """Open repo, package or modude in sublime."""
    subl_config = SublimeConfig(add=not new_window)

    if installed:
        search_path = None

    try:
        if not code:
            path = open_repo(name, search_path=search_path, subl_config=subl_config)

        else:
            path = open_code(
                name,
                search_path,
                installed=installed,
                subl_config=subl_config,
            ).path

    except (NotFoundError, MultipleFoundError) as error:
        print(error, file=sys.stderr)
        return 1

    print(f"Found `{name}` in  {path}.", file=sys.stderr)

    return 0
