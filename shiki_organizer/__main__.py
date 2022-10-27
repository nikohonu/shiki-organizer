import argparse
import datetime as dt
from datetime import date
from pathlib import Path

import appdirs
from termcolor import colored

from shiki_organizer.commands.overview_command import run_overview_command
from shiki_organizer.commands.add_command import (
    add_category_subparsers,
    add_field_subparsers,
    add_subparsers,
    run_add_category_command,
    run_add_command,
    run_add_field_command,
)
from shiki_organizer.commands.del_command import (
    del_category_subparsers,
    del_field_subparsers,
    del_subparsers,
    run_del_category_command,
    run_del_command,
    run_del_field_command,
)
from shiki_organizer.commands.do_command import do_subparsers, run_do_command
from shiki_organizer.commands.start_command import start_subparsers, run_start_command
from shiki_organizer.commands.stop_command import stop_subparsers, run_stop_command
from shiki_organizer.commands.edit_command import (
    edit_subparsers,
    run_edit_command,
    run_edit_field_command,
    run_edit_category_command,
    edit_field_subparsers,
    edit_category_subparsers,
)
from shiki_organizer.commands.list_command import (
    list_subparsers,
    run_list_command,
    tree_subparsers,
    run_tree_command,
)
from shiki_organizer.model import Task, Interval


def main():
    # processing
    for task in Task.select():
        if not task.is_completed and task.scheduled and task.scheduled < date.today():
            task.scheduled = date.today()
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
    # start
    parser = argparse.ArgumentParser(description="To-do list.")
    subparsers = parser.add_subparsers(help="sub-command help", dest="command")
    # task
    add_subparsers(subparsers)
    del_subparsers(subparsers)
    do_subparsers(subparsers)
    edit_subparsers(subparsers)
    list_subparsers(subparsers)
    tree_subparsers(subparsers)
    start_subparsers(subparsers)
    stop_subparsers(subparsers)
    # field
    del_field_subparsers(subparsers)
    add_field_subparsers(subparsers)
    edit_field_subparsers(subparsers)
    # category
    add_category_subparsers(subparsers)
    del_category_subparsers(subparsers)
    edit_category_subparsers(subparsers)
    args = parser.parse_args()
    data_path = Path(appdirs.user_data_dir("shiki-organizer", "Niko Honu"))
    tasks_path = data_path / "tasks"
    if not tasks_path.exists():
        tasks_path.mkdir(parents=True)
    match args.command:
        case "add-category":
            run_add_category_command(args, parser)
        case "add":
            run_add_command(args, parser)
        case "add-field":
            run_add_field_command(args, parser)
        case "del-category":
            run_del_category_command(args, parser)
        case "del":
            run_del_command(args, parser)
        case "del-field":
            run_del_field_command(args, parser)
        case "do":
            run_do_command(args, parser)
        case "list":
            run_list_command(args, parser)
        case "tree":
            run_tree_command(args, parser)
        case "edit":
            run_edit_command(args, parser)
        case "edit-field":
            run_edit_field_command(args, parser)
        case "edit-category":
            run_edit_category_command(args, parser)
        case "start":
            run_start_command(args, parser)
        case "stop":
            run_stop_command()
        case _:
            run_overview_command(args, parser)


if __name__ == "__main__":
    main()
