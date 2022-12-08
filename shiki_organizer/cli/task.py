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
@click.argument("description")
@click.option(
    "-p",
    "--priority",
    help="Priority of the task.",
    type=click.Choice(list(string.ascii_uppercase)),
)
@click.option(
    "-d",
    "--divider",
    default=1,
    help="Divider of the task.",
    type=click.IntRange(1),
)
@click.option(
    "-r",
    "--recurrence",
    help="Recurrence interval of the task.",
    type=click.IntRange(1),
)
@click.option(
    "-s",
    "--scheduled",
    is_flag=False,
    flag_value=str(dt.date.today()),
    help="Date when you plan to start working on this task.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "--deadline",
    is_flag=False,
    flag_value=str(dt.date.today()),
    help="Date when you plan to complete the work on this task.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "--parent",
    help="Id or uuid of the parent task.",
    type=str,
)
def add(description, priority, divider, recurrence, scheduled, deadline, parent):
    if parent:
        if parent.isnumeric():
            parent = Task.get_by_id(int(parent))
        else:
            parent = uuid.UUID(parent)
    task = Task.create(
        description=description,
        priority=priority,
        divider=divider,
        recurrence=recurrence,
        scheduled=scheduled.date() if scheduled else None,
        deadline=deadline.date() if deadline else None,
        parent=parent,
    )
    Task.reindex()
    task = Task.get_by_uuid(task.uuid)
    print(f"Created task {task.id}.")


@click.command()
@click.argument("task")
@click.option(
    "-n",
    "--description",
    help="Description of the task.",
    type=str,
)
@click.option(
    "-p",
    "--priority",
    is_flag=False,
    flag_value="",
    help="Priority of the task.",
    type=click.Choice(list(string.ascii_uppercase) + [""]),
)
@click.option(
    "-d",
    "--divider",
    is_flag=False,
    flag_value=1,
    help="Divider of the task.",
    type=click.IntRange(1),
)
@click.option(
    "-r",
    "--recurrence",
    is_flag=False,
    flag_value=0,
    help="Recurrence interval of the task.",
    type=int,
)
@click.option(
    "-s",
    "--scheduled",
    is_flag=False,
    flag_value="0001-01-01",
    help="Date when you plan to start working on this task.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "--deadline",
    is_flag=False,
    flag_value="0001-01-01",
    help="Date when you plan to complete the work on this task.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "--parent",
    help="Id or uuid of the parent task.",
    type=str,
)
def modify(task, description, priority, divider, recurrence, scheduled, deadline, parent):
    if task.isnumeric():
        task = Task.get_by_id(int(task))
    else:
        task = Task.get_by_uuid(uuid.UUID(task))
    description = task.description if description == None else description
    if priority == None:
        priority = task.priority
    elif priority == "":
        priority = None
    if divider == None:
        divider = task.divider
    if recurrence == None:
        recurrence = task.recurrence
    elif recurrence == 0:
        recurrence = None
    if scheduled == None:
        scheduled = task.scheduled
    elif scheduled == dt.datetime.min:
        scheduled = None
    else:
        scheduled = scheduled.date()
    if deadline == None:
        deadline = task.deadline
    elif deadline == dt.datetime.min:
        deadline = None
    else:
        deadline = deadline.date()
    q = task.update(
        description=description,
        priority=priority,
        divider=divider,
        recurrence=recurrence,
        scheduled=scheduled,
        deadline=deadline,
        parent=parent,
    ).where(Task.id == task.id)
    q.execute()
    print(f"Modifying task {task.id} '{task.description}'.")


@click.command()
@click.argument("task")
def delete(task):
    if task.isnumeric():
        task = Task.get_by_id(int(task))
    else:
        task = Task.get_by_uuid(uuid.UUID(task))
    Interval.delete().where(Interval.task == task).execute()
    task.delete_instance()
    print(f"Deleting task {task.id} '{task.description}'.")


@click.command()
@click.argument("task")
@click.option(
    "-s",
    "--start",
    type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%S"]),
    default=dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    help="Start of the interval",
)
@click.option(
    "-e",
    "--end",
    type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%S"]),
    help="End of the interval",
)
def start(task, start, end):
    if task.isnumeric():
        task = Task.get_by_id(int(task))
    else:
        task = Task.get_by_uuid(uuid.UUID(task))
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        if interval.task == task:
            print(get_status())
            return
        else:
            now = dt.datetime.now()
            interval.end = dt.datetime(
                now.year, now.month, now.day, now.hour, now.minute, now.second
            )
            interval.save()
            print(get_status("Recorded"))
    if end and end < start:
        end = None
        print("The end of the interval must be after the start.")
        return
    Interval.create(task=task, start=start, end=end)
    print(get_status())
    Interval.reindex()


@click.command()
def stop():
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        print(get_status("Recorded"))
        now = dt.datetime.now()
        interval.end = dt.datetime(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )
        interval.save()
    else:
        print("There is no active time tracking.")


@click.command()
def status():
    if Interval.get_or_none(Interval.end == None):
        print(get_status())
    else:
        print("There is no active time tracking.")


@click.command()
@click.argument("task")
@click.option("--github-token", default=lambda: os.environ.get("GITHUB_TOKEN", ""))
def done(task, github_token):
    if task.isnumeric():
        task = Task.get_by_id(int(task))
    else:
        task = Task.get_by_uuid(uuid.UUID(task))
    interval = Interval.get_or_none((Interval.end == None) & (Interval.task == task))
    if interval:
        print(get_status("Recorded"))
        interval.end = dt.datetime.now()
        interval.save()
    if task.recurrence:
        task.scheduled = (dt.datetime.now() + dt.timedelta(days=task.recurrence)).date()
        if task.deadline and task.scheduled > task.deadline:
            task.archived = True
            task.scheduled = dt.datetime.now()
    else:
        task.archived = True
    task.save()
    print(f"Completed task {task.id} '{task.description}'.")
    issue = Issue.get_or_none(Issue.task == task)
    if issue:
        if not github_token:
            print("GitHub token is required.")
            return
        g = Github(github_token)
        repo = g.get_repo(issue.repository.name)
        open_issues = repo.get_issues(state="open")
        for i in open_issues:
            if issue.number == i.number:
                i.edit(state="closed")
        print(f"Close issue {task.id} '{task.description}'.")


@click.command(name="ls")
@click.option(
    "-t", "--today", is_flag=True, default=False, help="Show only today tasks."
)
@click.option(
    "-a", "--archived", is_flag=True, default=False, help="Show archived task."
)
def ls(today, archived):
    def task_to_str(task):
        id = task.id if task.id else f"uuid:{task.uuid}"
        if task.priority:
            priority = f"{Fore.BLUE}({task.priority}){Style.RESET_ALL} "
        else:
            priority = ""
        if task.divider > 1:
            divider = f"{Fore.RED}({task.divider}){Style.RESET_ALL} "
        else:
            divider = ""
        scheduled = (
            f" {Fore.MAGENTA}scheduled:{Style.RESET_ALL}" + str(task.scheduled)
            if task.scheduled
            else ""
        )
        deadline = (
            f" {Fore.RED}deadline:{Style.RESET_ALL}" + str(task.deadline)
            if task.deadline
            else ""
        )
        recurrence = (
            f" {Fore.YELLOW}recurrence:{Style.RESET_ALL}{task.recurrence}d"
            if task.recurrence
            else ""
        )
        duration = (
            f" {Fore.GREEN}duration:{Style.RESET_ALL}{task.duration}d"
            if task.duration
            else ""
        )
        return f"{id} {priority}{divider}{task.description}{scheduled}{recurrence}{deadline}{duration}"

    tasks = None
    if not tasks:
        tasks = Task.select()
    if today:
        tasks = tasks.where(Task.scheduled == dt.date.today())
    else:
        tasks = Task.select()
    tasks = sorted(tasks, key=lambda x: x.priority if x.priority else "a")
    tasks = sorted(tasks, key=lambda x: x.scheduled if x.scheduled else dt.date.max)

    if not archived:
        tasks = filter(lambda x: not x.archived, tasks)
    for task in tasks:
        print(task_to_str(task))


@click.command()
def tags():
    tags = {}
    global_duration = 0
    for interval in Interval.select():
        for tag in interval.task.tags:
            duration = interval.duration
            if tag in tags:
                tags[tag] += duration
            else:
                tags[tag] = duration
            global_duration += duration
    tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
    for tag, duration in tags:
        print(
            tag.name,
            round(duration / 60 * 100) / 100,
            f"{round(duration / global_duration * 10000)/100}%",
        )


@click.command()
def projects():
    projects = {}
    global_duration = 0
    for interval in Interval.select():
        duration = interval.duration
        project = interval.task.project
        if project:
            if project in projects:
                projects[project] += duration
            else:
                projects[project] = duration
            global_duration += duration
    projects = sorted(projects.items(), key=lambda x: x[1], reverse=True)
    for project, duration in projects:
        print(
            project.name,
            round(duration / 60 * 100) / 100,
            f"{round(duration / global_duration * 10000)/100}%",
        )


@click.command()
def today():
    global_duration = 0
    for interval in Interval.select():
        if interval.start.date() == dt.date.today():
            global_duration += interval.duration
    print(f"{round(global_duration / 60 / 60 * 100) / 100}h")

    def process_issue(issues, repository, is_closed=False):
        for i in issues:
            issue, _ = Issue.get_or_create(number=i.number, repository=repository)
            issue.title = i.title
            if not issue.task:
                task = Task.create(
                    description=issue.title,
                )
                issue.task = task
            task = issue.task
            task.description = f"{issue.title} #{issue.number}"
            task.project = repository.project
            task.tags.clear()
            task.tags.add([repository.tag])
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
cli.add_command(modify)
cli.add_command(delete)
cli.add_command(start)
cli.add_command(stop)
cli.add_command(status)
cli.add_command(done)
cli.add_command(ls)
cli.add_command(tags)
cli.add_command(projects)
cli.add_command(today)


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
