import argparse
import datetime as dt
from datetime import date
from pathlib import Path

import appdirs
from termcolor import colored

from shiki_organizer.tasks import Tasks


def run_list_command(
    args: argparse.Namespace, parser: argparse.ArgumentParser, tasks: Tasks
):
    sorted_task = sorted(
        tasks.all().items(),
        key=lambda x: x[1].scheduled if x[1].scheduled != None else date.max,
    )
    for identifier, task in sorted_task:
        if vars(args).get("today") and args.today and task.scheduled != date.today():
            continue
        if task.is_completed:
            continue 
        scheduled = (
            colored(f" scheduled:", "red") + f"{task.scheduled}"
            if task.scheduled
            else ""
        )
        deadline = (
            colored(f" deadline:", "green") + f"{task.deadline}"
            if task.deadline
            else ""
        )
        recurrence = (
            colored(f" recurrence:", "yellow") + f"{task.recurrence}{task.unit}"
            if task.recurrence
            else ""
        )
        completions = colored(f" completions:", "blue") + f"{len(task.completions)}"
        print(f"{identifier}. {task.description}{scheduled}{deadline}{recurrence}{completions}")


def run_add_command(
    args: argparse.Namespace, parser: argparse.ArgumentParser, tasks: Tasks
):
    if args.recurrence and not args.unit:
        args.unit = "d"
    elif args.unit and not args.recurrence:
        parser.error("argument -u/--unit requires -r/--recurrence")
    scheduled = None
    deadline = None
    if args.scheduled:
        if args.scheduled == "today":
            scheduled = dt.date.today()
        else:
            try:
                scheduled: dt.date = dt.datetime.strptime(
                    args.scheduled, "%Y-%m-%d"
                ).date()
            except ValueError:
                parser.error(
                    "the format of the schedule is incorrect. Try this: YYYY-MM-DD"
                )
    if args.deadline:
        if args.deadline == "today":
            deadline = dt.date.today()
        else:
            try:
                deadline: dt.date = dt.datetime.strptime(
                    args.deadline, "%Y-%m-%d"
                ).date()
            except ValueError:
                parser.error(
                    "the format of the deadline is incorrect. Try this: YYYY-MM-DD"
                )
    if deadline and scheduled and deadline < scheduled:
        parser.error("the deadline cannot be earlier than scheduled")
    tasks.add(
        args.description,
        scheduled,
        deadline,
        args.recurrence,
        args.unit,
    )


def run_del_command(
    args: argparse.Namespace, parser: argparse.ArgumentParser, tasks: Tasks
):
    try:
        tasks.delete(args.id)
    except ValueError:
        parser.error("the task with this id does not exist")

def run_do_command(
    args: argparse.Namespace, parser: argparse.ArgumentParser, tasks: Tasks
):
    try:
        tasks.do(args.id)
    except ValueError:
        parser.error("the task with this id does not exist")


def run_edit_command(
    args: argparse.Namespace, parser: argparse.ArgumentParser, tasks: Tasks
):
    print(args)


def main():
    parser = argparse.ArgumentParser(description="To-do list.")
    subparsers = parser.add_subparsers(help="sub-command help", dest="command")
    parser_list = subparsers.add_parser("list", help="show tasks")
    parser_list.add_argument(
        "-t",
        "--today",
        action="store_true",
        help="show today task",
    )
    parser_add = subparsers.add_parser("add", help="add a task")
    parser_add.add_argument(
        "description", help="description of the task, aka name of the task"
    )
    parser_add.add_argument(
        "-s",
        "--scheduled",
        help="the date when you plan to start working on that task. Example: 2022-10-13",
    )
    parser_add.add_argument(
        "-d",
        "--deadline",
        help="the date when you plan to finish working on that task. Example: 2022-10-23",
    )
    parser_add.add_argument(
        "-r",
        "--recurrence",
        help="set the recurrence interval (the default unit is day, to change it use -u/--unit)",
        type=int,
    )
    parser_add.add_argument(
        "-u",
        "--unit",
        help="set the recurrence unit: d(day), w(week), m(month), y(year)",
        choices=["d", "w", "m", "y"],
    )
    parser_del = subparsers.add_parser("del", help="delete the task")
    parser_del.add_argument("id", help="the task id", type=int)
    parser_do = subparsers.add_parser("do", help="complete the task")
    parser_do.add_argument("id", help="the task id", type=int)
    parser_edit = subparsers.add_parser("edit", help="edit the task")
    args = parser.parse_args()
    data_path = Path(appdirs.user_data_dir("shiki-organizer", "Niko Honu"))
    tasks_path = data_path / "tasks"
    if not tasks_path.exists():
        tasks_path.mkdir(parents=True)
    tasks = Tasks(tasks_path)
    match args.command:
        case "list":
            run_list_command(args, parser, tasks)
        case "add":
            run_add_command(args, parser, tasks)
        case "del":
            run_del_command(args, parser, tasks)
        case "do":
            run_do_command(args, parser, tasks)
        case "edit":
            run_edit_command(args)
        case _:
            run_list_command(args, parser, tasks)


if __name__ == "__main__":
    main()
