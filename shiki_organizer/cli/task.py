import copy
import datetime as dt

import click
from click_aliases import ClickAliasedGroup

from shiki_organizer.cli.formatting import duration_to_str, get_table, get_tree
from shiki_organizer.formatting import console
from shiki_organizer.models.task import (
    add_task,
    delete_task,
    get_current_interval,
    get_task_by_id,
    get_task_ids,
    get_tasks,
    modify_task,
    start_task,
    stop_task,
    str_tag_to_tuple,
    tag_task,
    untag_task,
)


@click.group(cls=ClickAliasedGroup)
def task():
    pass


@task.command()
@click.argument("name", nargs=-1)
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
@click.option(
    "-t",
    "--tag",
    "tags",
    type=str,
    multiple=True,
    help='Tags for the task. For example, "type:media" or just "media". You '
    'can also specify multiple tags with "-t tag1 -t tag2"',
)
def add(name, notes, parent_id, order, scheduled, recurrence, want, tags):
    """Add a task with a NAME."""
    if len(name) == 0:
        console.print("Error: Missing argument 'NAME'.")
        return
    name = " ".join(name)
    scheduled = scheduled.date() if scheduled else None
    want *= 60
    task = add_task(name, notes, parent_id, order, scheduled, recurrence, want, tags)
    console.print(f'"{task.id} {task.name}" was created.')


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
    want *= 60
    task = modify_task(
        int(id), name, notes, parent_id, order, scheduled, recurrence, want
    )
    console.print(f'"{task.id} {task.name}" was modified.')


@task.command(aliases=["delete", "del"])
@click.argument("ids", type=click.Choice([str(id) for id in get_task_ids()]), nargs=-1)
def delete(ids):
    """Delete tasks with IDS."""
    tasks = delete_task(ids)
    for task in tasks:
        console.print(f'"{task["id"]} {task["name"]}" was deleted.')


@task.command()
@click.argument("ids", type=click.Choice([str(id) for id in get_task_ids()]), nargs=-1)
def show():
    pass


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
def tree(period, individual, completed, sorting, reverse):
    tasks = get_tasks(True, period, individual, completed, sorting, reverse)
    tree = get_tree(tasks)
    console.print(tree)


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
    "next_tasks",
    is_flag=True,
    help="Show tasks that are scheduled to start today or earlier.",
)
def table(period, individual, completed, sorting, reverse, next_tasks):
    tasks = get_tasks(True, period, individual, completed, sorting, reverse)
    tasks = (
        list(
            filter(
                lambda t: next(iter(t["tags"]["scheduled"])) <= dt.date.today()
                if "scheduled" in t["tags"]
                else False,
                tasks,
            )
        )
        if next_tasks
        else tasks
    )
    tree = get_table(tasks)
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
    start_task(int(id), start, end)
    get_current_task_status()


@task.command()
def stop():
    get_current_task_status()
    stop_task()


@task.command()
@click.argument("id", type=click.Choice([str(id) for id in get_task_ids()]))
@click.argument("raw_tags", type=str, nargs=-1)
def tag(id, raw_tags):
    tags = set()
    for raw_tag in raw_tags:
        tags.add(str_tag_to_tuple(raw_tag))
    tag_task(get_task_by_id(id), tags)


@task.command()
@click.argument("id", type=click.Choice([str(id) for id in get_task_ids()]))
@click.argument("raw_tags", type=str, nargs=-1)
def untag(id, raw_tags):
    tags = set()
    for raw_tag in raw_tags:
        tags.add(str_tag_to_tuple(raw_tag))
    untag_task(get_task_by_id(id), tags)


@task.command()
@click.argument("ids", type=click.Choice([str(id) for id in get_task_ids()]), nargs=-1)
def done(ids):
    get_current_task_status()
    stop_task()
    tasks = get_tasks(True)
    tasks = list(filter(lambda t: str(t["id"]) in ids, tasks))
    for task in tasks:
        status = (
            next(iter(task["tags"]["status"])) if "status" in task["tags"] else None
        )
        if status == "completed":
            return
        recurrence = (
            next(iter(task["tags"]["recurrence"]))
            if "recurrence" in task["tags"]
            else None
        )
        scheduled = (
            next(iter(task["tags"]["scheduled"]))
            if "scheduled" in task["tags"]
            else None
        )
        deadline = (
            next(iter(task["tags"]["deadline"])) if "deadline" in task["tags"] else None
        )
        if recurrence:
            scheduled = (dt.datetime.now() + dt.timedelta(days=recurrence)).date()
            if deadline and scheduled > deadline:
                status = "completed"
                scheduled = dt.date.today()
        else:
            status = "completed"
        tags = set()
        task = get_task_by_id(task["id"])
        untag_task(task, {("scheduled", "*"), ("deadline", "*"), ("status", "*")})
        tags.add(("scheduled", scheduled)) if scheduled else None
        tags.add(("deadline", deadline)) if deadline else None
        tags.add(("status", status)) if status else None
        tag_task(task, tags)


@task.command()
def status():
    get_current_task_status()
