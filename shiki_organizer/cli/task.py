import copy
import datetime as dt

import click
from click_aliases import ClickAliasedGroup

from shiki_organizer.cli.datetime import period_to_datetime
from shiki_organizer.cli.style import duration_to_str
from shiki_organizer.cli.table import create_tasks_table
from shiki_organizer.cli.tree import create_tasks_tree
from shiki_organizer.formatting import console
from shiki_organizer.models.task import add_task, get_task_ids, modify_task


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
    "-t",
    "--tag",
    "tags",
    type=str,
    multiple=True,
    help='Tags for the task. For example, "type:media" or just "media". You '
    'can also specify multiple tags with "-t tag1 -t tag2"',
)
def add(name, notes, parent_id, order, scheduled, recurrence, tags):
    """Add a task with a NAME."""
    if len(name) == 0:
        console.print("Error: Missing argument 'NAME'.")
        return
    name = " ".join(name)
    scheduled = scheduled.date() if scheduled else None
    task = add_task(name, notes, parent_id, order, scheduled, recurrence, tags)
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
def modify(id, name, notes, parent_id, order, scheduled, recurrence):
    """Modify the task with the ID. This command can only modify properties; to
    remove properties, use the untag command instead. For example, "so task
    untag ID scheldued:*" """
    scheduled = scheduled.date() if scheduled else None
    task = modify_task(int(id), name, notes, parent_id, order, scheduled, recurrence)
    console.print(f'"{task.id} {task.name}" was modified.')


# def _calc_duration(tasks, period, all_days=False):
#     def get_task(task_id):
#         for task in tasks:
#             if task["id"] == task_id:
#                 return task
#
#     start = dt.datetime.max
#     intervals = so_task.get_intervals()
#     for interval in intervals:
#         if interval["start"] < start:
#             start = interval["start"]
#     start = period_to_datetime(period, start)
#     intervals = filter(lambda interval: interval["start"] >= start, intervals)
#     for interval in intervals:
#         result = []
#         queue = [get_task(interval["task_id"])]
#         while queue:
#             task = queue.pop()
#             result.append(task)
#             if task:
#                 if "parent" in task:
#                     queue.append(get_task(task["parent"]))
#         for task in result:
#             if task:
#                 if "duration" in task:
#                     task["duration"] += interval["duration"]
#                 else:
#                     task["duration"] = interval["duration"]
#                 if "days" in task:
#                     task["days"].add(interval["start"].date())
#                 else:
#                     task["days"] = {interval["start"].date()}
#     for task in tasks:
#         if "days" in task:
#             if all_days:
#                 task["days"] = (dt.datetime.now() - start).days + 1
#             else:
#                 task["days"] = len(task["days"])
#             task["average"] = round(task["duration"] / task["days"])
#     return start
#
#
#
#
# @task.command()
# def test():
#     for task in so_task.all():
#         console.print(_process_raw_task(task))
#
#
# def process_raw_tag(raw_tag):
#     if raw_tag.find(":") != -1:
#         tag = tuple(raw_tag.split(":", 1))
#     else:
#         tag = ("", raw_tag)
#     return tag
#
#
#
#
# @task.command()
# @click.argument(
#     "task_ids", type=click.Choice([str(id) for id in so_task.get_ids()]), nargs=-1
# )
# def delete(task_ids):
#     for task_id in task_ids:
#         id, name = so_task.delete(int(task_id))
#         console.print(f'{id} "{name}" deleted.')
#
#
# @task.command()
# @click.option("-t", "--tree", is_flag=True, default=False, help="Show tasks as tree.")
# @click.option(
#     "-s",
#     "--sort",
#     default="duration",
#     type=click.Choice(
#         ["duration", "average", "scheduled", "deadline", "days", "recurrence"]
#     ),
#     help="Sort by field.",
# )
# @click.option(
#     "-r",
#     "--reverse",
#     is_flag=True,
#     default=False,
#     help="Reverse the task sorting",
# )
# @click.option(
#     "-d",
#     "--days",
#     is_flag=True,
#     default=False,
#     help="Days are counted for all tasks starting from the earliest interval",
# )
# @click.option(
#     "-c", "--completed", is_flag=True, default=False, help="Show completed task."
# )
# @click.option("-n", "--next", is_flag=True, default=False, help="Show next tasks.")
# @click.option(
#     "-p",
#     "--period",
#     type=click.Choice(["all", "today", "week", "month", "year"]),
#     default="all",
#     help="Show data only for this period of time.",
# )
# def show(tree, completed, days, reverse, sort, next, period):
#     tasks = [_process_raw_task(raw_task) for raw_task in so_task.all()]
#     _calc_duration(tasks, period, days)
#     if not completed:
#         tasks = list(
#             filter(
#                 lambda task: ("status" not in task)
#                 or ("status" in task and task["status"] != "completed"),
#                 tasks,
#             )
#         )
#     if next:
#         tasks = list(
#             filter(
#                 lambda task: "scheduled" in task
#                 and task["scheduled"] <= dt.date.today(),
#                 tasks,
#             )
#         )
#     if sort in ["scheduled", "deadline"]:
#         tasks = sorted(
#             tasks,
#             key=lambda task: task[sort] if sort in task else dt.date.min,
#             reverse=not reverse,
#         )
#     else:
#         tasks = sorted(
#             tasks,
#             key=lambda task: task[sort] if sort in task else 0,
#             reverse=not reverse,
#         )
#     if tree:
#         result = create_tasks_tree(tasks)
#     else:
#         result = create_tasks_table(tasks)
#     console.print(result)
#
#
# @task.command()
# @click.argument("task_id", type=click.Choice([str(id) for id in so_task.get_ids()]))
# @click.option(
#     "-s",
#     "--start",
#     type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%S"]),
#     default=dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
#     help="Start of the interval",
# )
# @click.option(
#     "-e",
#     "--end",
#     type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%S"]),
#     help="End of the interval",
# )
# def start(task_id, start, end):
#     so_task.start(int(task_id), start, end)
#     get_current_task_status()
#
#
# @task.command()
# def stop():
#     get_current_task_status()
#     so_task.stop()
#
#
# @task.command()
# @click.argument("task_id", type=click.Choice([str(id) for id in so_task.get_ids()]))
# @click.argument("raw_tags", type=str, nargs=-1)
# def tag(task_id, raw_tags):
#     tags = set()
#     for raw_tag in raw_tags:
#         tags.add(process_raw_tag(raw_tag))
#     so_task.tag(task_id, tags)
#
#
# @task.command()
# @click.argument("task_id", type=click.Choice([str(id) for id in so_task.get_ids()]))
# @click.argument("raw_tags", type=str, nargs=-1)
# def untag(task_id, raw_tags):
#     tags = set()
#     for raw_tag in raw_tags:
#         tags.add(process_raw_tag(raw_tag))
#     so_task.untag(task_id, tags)
#
#
# def get_current_task_status():
#     interval = so_task.get_current_interval()
#     if interval:
#         task = so_task.get_by_id(interval["task_id"])
#         result = ""
#         result = f"{task['id']} \"{task['name']}\""
#         result += f" from {interval['start'].strftime('%T')}"
#         result += f" to {dt.datetime.now().strftime('%T')}"
#         result += f" duration is {duration_to_str(interval['duration'])}."
#         console.print(result)
#
#
# @task.command()
# @click.argument(
#     "task_ids", type=click.Choice([str(id) for id in so_task.get_ids()]), nargs=-1
# )
# def done(task_ids):
#     get_current_task_status()
#     so_task.stop()
#     tasks = [_process_raw_task(raw_task) for raw_task in so_task.all(task_ids)]
#     for task in tasks:
#         status = task["status"] if "status" in task else None
#         if status == "completed":
#             return
#         recurrence = task["recurrence"] if "recurrence" in task else None
#         scheduled = task["scheduled"] if "scheduled" in task else None
#         deadline = task["deadline"] if "deadline" in task else None
#         if recurrence:
#             scheduled = (dt.datetime.now() + dt.timedelta(days=recurrence)).date()
#             if deadline and scheduled > deadline:
#                 status = "completed"
#                 scheduled = dt.date.today()
#         else:
#             status = "completed"
#         tags = set()
#         so_task.untag(
#             task["id"], [("scheduled", "*"), ("deadline", "*"), ("status", "*")]
#         )
#         tags.add(("scheduled", scheduled)) if scheduled else None
#         tags.add(("deadline", deadline)) if deadline else None
#         tags.add(("status", status)) if status else None
#         so_task.tag(task["id"], tags)
#
#
# @task.command()
# def status():
#     get_current_task_status()
