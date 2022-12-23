import datetime as dt
import os
import string
import uuid

import click

from shiki_organizer.actions import get_status
from shiki_organizer.model import Interval, Task
import shiki_organizer.actions as actions
from shiki_organizer.cli.formatter import task_to_str
from shiki_organizer.datetime import period_to_datetime


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
    is_flag=False,
    flag_value="",
    help="Id or uuid of the parent task.",
    type=str,
)
def modify(
    task, description, priority, divider, recurrence, scheduled, deadline, parent
):
    if task.isnumeric():
        task = Task.get_by_id(int(task))
    else:
        task = Task.get_by_uuid(uuid.UUID(task))
    if parent:
        if parent.isnumeric():
            parent = Task.get_by_id(int(parent))
        else:
            parent = uuid.UUID(parent)
    elif parent == "":
        parent = None
    else:
        parent = task.parent

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
    actions.start(task, start, end)


@click.command()
def stop():
    actions.stop()


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
    actions.done([task], github_token)


def _update_tasks(start):
    query = Task.update(duration=0, days=0)
    query.execute()
    intervals = Interval.select().where(Interval.start >= start)
    items = {}
    for interval in intervals:
        task = interval.task
        while task:
            if task.id not in items:
                items[task.id] = {"task": task, "duration": 0, "days": 0}
                items[task.id]["duration"] = interval.duration
                items[task.id]["days"] = set([interval.start.date()])
            else:
                items[task.id]["duration"] += interval.duration
                items[task.id]["days"].add(interval.start.date())
            task = task.parent
    tasks = []
    for item in items:
        task = items[item]["task"]
        task.days = len(items[item]["days"])
        task.duration = items[item]["duration"]
        tasks.append(task)
    Task.bulk_update(tasks, fields=[Task.duration, Task.days])


@click.command()
@click.option(
    "-t", "--today", is_flag=True, default=False, help="Show only today tasks."
)
@click.option(
    "-a", "--archived", is_flag=True, default=False, help="Show archived task."
)
@click.option(
    "-u", "--uuid", is_flag=True, default=False, help="Show uuid of interval."
)
def ls(today, archived, uuid):
    tasks = Task.select()
    if today:
        tasks = sorted(
            tasks.where(Task.scheduled <= dt.date.today()),
            key=lambda x: x.priority if x.priority else "a",
        )
    else:
        tasks = sorted(tasks, key=lambda x: x.scheduled if x.scheduled else dt.date.max)
    if not archived:
        tasks = filter(lambda x: not x.archived, tasks)
    for task in tasks:
        print(task_to_str(task, uuid))


@click.command()
@click.option(
    "-p",
    "--period",
    type=click.Choice(["all", "today", "week", "month", "year"]),
    default="all",
    help="Show data only for this period of time.",
)
@click.option(
    "-a", "--archived", is_flag=True, default=False, help="Show archived task."
)
@click.option(
    "-u", "--uuid", is_flag=True, default=False, help="Show uuid of interval."
)
@click.option(
    "-d", "--duration", is_flag=True, default=False, help="Hide task without duration."
)
@click.option("-r", "--root", help="Set the root task of tree.")
def tree(period, archived, uuid, root, duration):
    start = period_to_datetime(period)
    if root:
        if root.isnumeric():
            root = Task.get_by_id(int(root))
        else:
            root = Task.get_by_uuid(uuid.UUID(root))
    _update_tasks(start)
    tasks = sorted(
        Task.select().where((Task.parent == root)),
        key=lambda x: x.duration,
    )
    queue = [(0, task) for task in tasks]
    while queue:
        item = queue.pop()
        if duration and item[1].duration == 0:
            continue
        if item[1].archived == False or archived:
            tasks = sorted(
                Task.select().where((Task.parent == item[1])),
                key=lambda x: x.duration,
            )
            queue += [(item[0] + 1, task) for task in tasks]
            space = "\t"
            print(f"{space * item[0]}{task_to_str(item[1], uuid)}")


@click.command()
def reindex():
    Task.reindex()


cli.add_command(add)
cli.add_command(modify)
cli.add_command(delete)
cli.add_command(start)
cli.add_command(stop)
cli.add_command(status)
cli.add_command(done)
cli.add_command(ls)
cli.add_command(tree)
cli.add_command(reindex)


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
