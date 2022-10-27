import argparse
import datetime as dt

from termcolor import colored

from shiki_organizer.model import Interval


def stop_subparsers(subparsers: argparse._SubParsersAction):
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "stop", help="stop a task"
    )

def run_stop_command():
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        interval.end = dt.datetime.now()
        interval.save()
