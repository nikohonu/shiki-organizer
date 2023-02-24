import copy
import datetime as dt

import click
from click_aliases import ClickAliasedGroup

from shiki_organizer.cli.formatting import duration_to_str, get_tree
from shiki_organizer.formatting import console
from shiki_organizer.models.task import (
    add_task,
    delete_task,
    done_tasks,
    get_current_interval,
    get_task,
    get_task_by_id,
    get_task_ids,
    get_tasks,
    modify_task,
    start_task,
    stop_task,
    str_tag_to_tuple,
    tag_task,
    tag_task_by_strings,
    untag_task,
    untag_task_by_strings,
)


@click.group(cls=ClickAliasedGroup)
def task():
    pass


@task.command()
@click.argument("name")
@click.option(
    "-n", "--notes", type=str, help="Any additional information about the task."
)
@click.option(
    "-p",
    "--parent",
    "parent_id",
    type=click.Choice([str(id) for id in get_task_ids()]),
    help="The ID of the parent task.",
)
@click.option(
    "-o",
    "--order",
    type=click.IntRange(0),
    help="The order of the task.",
)
@click.option(
    "-s",
    "--scheduled",
    is_flag=False,
    flag_value=str(dt.date.today()),
    help="Scheduled date of execution.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "-r",
    "--recurrence",
    type=click.IntRange(1),
    help="Task recurrence interval in days.",
)
@click.option(
    "-w",
    "--want",
    type=click.IntRange(1),
    help="How much time on average you want to spend on this task (in minutes).",
)
def add(name, notes, parent_id, order, scheduled, recurrence, want):
    """Add a task with a NAME."""
    scheduled = scheduled.date() if scheduled else None
    want = dt.timedelta(minutes=want) if want else None
    task = add_task(name, notes, parent_id, order, scheduled, recurrence, want)
    console.print(task.id, f'"{task.name}" was created.')


@task.command(aliases=["modify", "mod"])
@click.argument("id", type=click.Choice([str(id) for id in get_task_ids()]))
@click.option("-d", "--name", type=str, help="Name of the task")
@click.option(
    "-n", "--notes", type=str, help="Any additional information about the task."
)
@click.option(
    "-p",
    "--parent",
    "parent_id",
    type=click.Choice([str(id) for id in get_task_ids()]),
    help="The ID of the parent task.",
)
@click.option(
    "-o",
    "--order",
    type=click.IntRange(0),
    help="The order of the task.",
)
@click.option(
    "-s",
    "--scheduled",
    is_flag=False,
    flag_value=str(dt.date.today()),
    help="Scheduled date of execution.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "-r",
    "--recurrence",
    type=click.IntRange(1),
    help="Task recurrence interval in days.",
)
@click.option(
    "-w",
    "--want",
    type=click.IntRange(1),
    help="How much time on average you want to spend on this task (in minutes).",
)
def modify(id, name, notes, parent_id, order, scheduled, recurrence, want):
    """Modify the task with the ID. This command can only modify properties; to
    remove properties, use the untag command instead. For example, "so task
    untag ID scheldued:*" """
    scheduled = scheduled.date() if scheduled else None
    want = dt.timedelta(minutes=want) if want else None
    task = modify_task(
        int(id), name, notes, parent_id, order, scheduled, recurrence, want
    )
    console.print(task.id, f'"{task.name}" was modified.')


@task.command()
@click.argument("ids", type=click.Choice([str(id) for id in get_task_ids()]), nargs=-1)
def done(ids):
    """Stop task tracking and complete or reschedule the task with IDS."""
    get_current_task_status()
    results = done_tasks(ids)
    for id, name, result in results:
        console.print(id, f'"{name}" was {result}.')


@task.command(aliases=["delete", "del"])
@click.argument("ids", type=click.Choice([str(id) for id in get_task_ids()]), nargs=-1)
def delete(ids):
    """Delete tasks with IDS."""
    tasks = delete_task(ids)
    for task in tasks:
        console.print(task["id"], f'{task["name"]}" was deleted.')


@task.command()
@click.argument("id", type=click.Choice([str(id) for id in get_task_ids()]))
def show(id):
    """Show information about a task with an ID."""
    task = get_task(int(id))
    console.print(task)


@task.command()
@click.option(
    "-p",
    "--period",
    type=click.Choice(["all", "day", "week", "month", "year"]),
    default="all",
    help="The period for calculating the duration and average duration of tasks.",
)
@click.option(
    "-i",
    "--individual",
    is_flag=True,
    help="Use an individual average for the task, i.e., divide the duration by"
    "the days on which you track the task",
)
@click.option(
    "-c",
    "--completed",
    is_flag=True,
    help="Show completed tasks.",
)
@click.option(
    "-s",
    "--sorting",
    default="duration",
    type=click.Choice(
        [
            "want",
            "need",
            "duration",
            "average",
            "scheduled",
            "days",
            "recurrence",
        ]
    ),
    help="Sort by the field.",
)
@click.option(
    "-r",
    "--reverse",
    is_flag=True,
    help="Reverse sorting.",
)
@click.option(
    "-n",
    "--next",
    is_flag=True,
    help="Show tasks that are scheduled to start today or earlier.",
)
def tree(period, individual, completed, sorting, reverse, next):
    """Show the task tree."""
    query = []
    if next:
        query.append(("scheduled", "<=", dt.date.today()))
    tasks = get_tasks(query, period, individual, sorting, completed, reverse)
    tree = get_tree(0, tasks)
    console.print(tree)


def get_current_task_status():
    interval = get_current_interval()
    if interval:
        task = interval.task
        result = ""
        result = f'{task.id} "{task.name}"'
        result += f" from {interval.start.strftime('%T')}"
        result += f" to {dt.datetime.now().strftime('%T')}"
        duration = duration_to_str(interval.duration)
        result += f" duration is {duration if duration else '0s'}."
        console.print(result)
    else:
        console.print("You don't have a current task.")


@task.command()
@click.argument("id", type=click.Choice([str(id) for id in get_task_ids()]))
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
def start(id, start, end):
    """Start task tracking with ID."""
    start_task(int(id), start, end)
    get_current_task_status()


@task.command()
def stop():
    """Stop task tracking.."""
    get_current_task_status()
    stop_task()


@task.command()
@click.argument("id", type=click.Choice([str(id) for id in get_task_ids()]))
@click.argument("tags", type=str, nargs=-1)
def tag(id, tags):
    """Add tags to the task."""
    tag_task_by_strings(get_task_by_id(id), tags)


@task.command()
@click.argument("id", type=click.Choice([str(id) for id in get_task_ids()]))
@click.argument("tags", type=str, nargs=-1)
def untag(id, tags):
    """Remove tags from the task."""
    untag_task_by_strings(get_task_by_id(id), tags)


@task.command()
def status():
    """Show information about the current task."""
    get_current_task_status()
