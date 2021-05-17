from pathlib import Path

import click

from pyutils.callgraph.pyan import create_callgraph
from pyutils.subl import open_module


@click.command()
@click.argument('import_statement', nargs=1, type=str)
@click.option('--fmt', '-f', nargs=1, type=str, default='svg')
@click.option('--parent_path', '-p', nargs=1, type=str,
              default=Path.home() / 'Repos')
@click.option('--installed', '-i', is_flag=True)
@click.option('--output-path', '-d', type=str,
              default=Path.home() / 'Pictures' / 'Graphs')
@click.option('--output-filename', '-o', type=str, default='myuses')
def make_callgraph(import_statement, fmt, parent_path, installed, output_path,
                   output_filename):
    # TODO: add yml config file
    # TODO: add open_cmd
    # TODO: add graph controls to arg
    # TODO: add help

    create_callgraph(import_statement, fmt=fmt, parent_path=parent_path,
                     installed=installed, output_path=output_path,
                     output_filename=output_filename)


@click.command()
@click.argument('import_statement', nargs=1, type=str)
@click.option('--parent_path', '-p', nargs=1, type=str,
              default=Path.home() / 'Repos')
@click.option('--installed', '-i', is_flag=True)
@click.option('--new-window', '-n', is_flag=True)
def open_module_subl(import_statement, parent_path, installed, new_window):
    open_module(import_statement, parent_path=parent_path,
                installed=installed, add=not new_window)
