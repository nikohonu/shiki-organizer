import datetime as dt
import os
import string
import uuid

import click
from colorama import Fore, Style
from github import Github

from shiki_organizer.actions import get_status
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
def ls():
    for repository in Repository.select():
        print(
            repository.id,
            repository.name,
            f"parent:{repository.task.description}",
        )


@click.command()
@click.argument("id", type=int)
def delete(id):
    repository = Repository.get_or_none(id)
    repository.delete_instance()


@click.command()
@click.option(
    "--github-token", default=lambda: os.environ.get("GITHUB_TOKEN", ""), required=True
)
def pull(github_token):
    def process_issue(issues, repository, is_closed=False):
        for i in issues:
            issue, _ = Issue.get_or_create(id=i.number, repository=repository)
            issue.title = i.title
            if not issue.task:
                task = Task.create(
                    description=issue.title,
                )
                issue.task = task
            task = issue.task
            task.description = f"{issue.title} #{issue.id}"
            task.parent = repository.parent
            task.archived = is_closed
            task.save()
            issue.save()
            Task.reindex()

    if not github_token:
        print("GitHub token is required.")
        return
    g = Github(github_token)

    for repository in Repository.select():
        repo = g.get_repo(repository.name)
        open_issues = repo.get_issues(state="open")
        closed_issues = repo.get_issues(state="closed")
        process_issue(open_issues, repository)
        process_issue(closed_issues, repository, True)


cli.add_command(add)
cli.add_command(ls)
cli.add_command(delete)
cli.add_command(pull)


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
