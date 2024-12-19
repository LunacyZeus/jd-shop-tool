import click

from pkg.solution.run import start_run

@click.group()
def solution_cli():
    pass


@solution_cli.command()
def run():
    """[cli] start_run """
    start_run()
