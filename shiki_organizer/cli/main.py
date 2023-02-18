import click

from shiki_organizer.cli.interval import interval
from shiki_organizer.cli.task import task


@click.group()
def cli():
    pass


cli.add_command(task)
cli.add_command(interval)


def main():
    cli()
