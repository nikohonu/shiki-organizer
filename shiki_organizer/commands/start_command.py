import argparse
import datetime as dt

from termcolor import colored

from shiki_organizer.commands.stop_command import run_stop_command
from shiki_organizer.model import Interval, Task


def start_subparsers(subparsers: argparse._SubParsersAction):
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "start", help="start the task"
    )
    parser.add_argument("id", help="the task id", type=int, choices=[t.id for t in Task.select()])


def run_start_command(
    args: argparse.Namespace, parser: argparse.ArgumentParser
):
    task = Task.get_by_id(args.id)
    interval = Interval.get_or_none(Interval.end == None)
    if not interval:
        Interval.create(task=task)
    else:
        print("You need to stop the previous task before starting a new one.")
