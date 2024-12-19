import click

from cli.solution import solution_cli

cli = click.CommandCollection(sources=[solution_cli,])

if __name__ == '__main__':
    cli()
