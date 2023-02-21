import copy
import datetime as dt

import click
from rich.console import Console

import shiki_organizer.models.task as so_task
from shiki_organizer.cli.formatting import get_intervals
from shiki_organizer.cli.table import create_intervals_table

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
    data = []
    intervals = get_intervals()
    for interval in intervals:
        # interval["end"] = interval["end"].strftime("%Y-%m-%d %H:%M:%S")
        data.append(
            {
                "id": interval.id,
                "task_id": interval.task.id,
                "name": interval.task.name,
                "start": interval.start,
                "end": interval.end if interval.end else dt.datetime.now(),
                "duration": interval.duration,
            }
        )
    table = create_intervals_table(data)
    console.print(table)
