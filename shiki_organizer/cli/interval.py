import copy
import datetime as dt

import click
from rich.console import Console

import shiki_organizer.models.task as so_task
from shiki_organizer.cli.datetime import period_to_datetime
from shiki_organizer.cli.style import duration_to_str
from shiki_organizer.cli.table import create_intervals_table
from shiki_organizer.cli.tree import create_tasks_tree

console = Console()


@click.group()
def interval():
    pass


def sort_dict_in_list(dicts, keys):
    result = []
    for d in dicts:
        result.append({k: d[k] for k in keys})
    return result


@interval.command()
def show():
    tasks = so_task.all()

    def get_task_name(task_id):
        for task in tasks:
            if task["id"] == task_id:
                return task["name"]

    intervals = so_task.get_intervals()
    for interval in intervals:
        interval["name"] = get_task_name(interval["task_id"])
        if "end" in interval and interval["end"]:
            interval["end"] = interval["end"].strftime("%Y-%m-%d %H:%M:%S")
    intervals = sort_dict_in_list(
        intervals, ["id", "task_id", "name", "start", "end", "duration"]
    )
    table = create_intervals_table(intervals)
    console.print(table)
