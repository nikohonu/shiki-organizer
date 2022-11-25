import argparse
import datetime as dt

from termcolor import colored

from shiki_organizer.commands.stop_command import run_stop_command
from shiki_organizer.model import Task


def do_subparsers(subparsers: argparse._SubParsersAction):
    parser_do: argparse.ArgumentParser = subparsers.add_parser(
        "do", help="complete the task"
    )
    parser_do.add_argument(
        "id", help="the task id", type=int, choices=[t.id for t in Task.select()]
    )


def run_do_command(args: argparse.Namespace, parser: argparse.ArgumentParser):
    task = Task.get_by_id(args.id)
    if task.recurrence:
        task.scheduled = (dt.datetime.now() + dt.timedelta(days=task.recurrence)).date()
        if task.deadline and task.scheduled > task.deadline:
            task.is_completed = True
            task.scheduled = dt.datetime.now()
    else:
        task.is_completed = True
    task.save()
    run_stop_command()