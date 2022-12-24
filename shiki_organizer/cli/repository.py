import datetime as dt
import os
import uuid

import click
from github import Github

import shiki_organizer.actions as actions
from shiki_organizer.model import Interval, Issue, Repository, Task


@click.group()
def cli():
    pass


@click.command()
@click.argument("name")
@click.option(
    "-p",
    "--parent",
    help="Id or uuid of the parent task.",
    type=str,
)
def add(name, parent):
    if parent.isnumeric():
        parent = Task.get_by_id(int(parent))
    else:
        parent = Task.get_by_uuid(uuid.UUID(parent))
    repository = Repository.create(name=name, parent=parent)
    Repository.reindex()
    print(f"Added repository {repository.name}.")


@click.command()
@click.argument("repository")
@click.option(
    "-n",
    "--name",
    help="Name of the repository on GitHub in format 'user/projects'.",
    type=str,
)
@click.option(
    "-p",
    "--parent",
    is_flag=False,
    flag_value="",
    help="Id or uuid of the parent task.",
    type=str,
)
def modify(repository, name, parent):
    if repository.isnumeric():
        repository = Repository.get_by_id(int(repository))
    else:
        repository = Repository.get_by_uuid(uuid.UUID(repository))
    if parent:
        if parent.isnumeric():
            parent = Task.get_by_id(int(parent))
        else:
            parent = uuid.UUID(parent)
    elif parent == "":
        parent = None
    else:
        parent = repository.parent
    name = repository.name if name == None else name
    q = Repository.update(
        name=name,
        parent=parent,
    ).where(Repository.id == repository.id)
    q.execute()
    print(f"Modifying repository {repository.id} '{name}'.")


@click.command()
def ls():
    for repository in Repository.select():
        parent_id = (
            repository.parent.id if repository.parent.id else repository.parent.uuid
        )
        print(
            repository.id,
            repository.name,
            f"parent:{parent_id} {repository.parent.description}",
        )


@click.command()
@click.argument("id", type=int)
def delete(id):
    repository = Repository.get_or_none(id)
    repository.delete_instance()


@click.command()
def pull():
    print(actions.pull())


cli.add_command(add)
cli.add_command(ls)
cli.add_command(delete)
cli.add_command(pull)
cli.add_command(modify)


def main():
    # processing
    for task in Task.select():
        if not task.archived and task.scheduled and task.scheduled < dt.date.today():
            task.scheduled = dt.date.today()
            task.save()
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        while interval.start.date() != dt.date.today():
            interval.end = dt.datetime.combine(interval.start.date(), dt.time.max)
            interval.save()
            next_day_datetime = dt.datetime.combine(
                interval.start.date() + dt.timedelta(days=1), dt.time.min
            )
            interval = Interval.create(task=interval.task, start=next_day_datetime)
        interval.save()
    cli()


if __name__ == "__main__":
    main()
