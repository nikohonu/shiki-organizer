import argparse
import datetime as dt

from termcolor import colored

from shiki_organizer.model import Field, Interval, Task


def run_overview_command(args: argparse.Namespace, parser: argparse.ArgumentParser):
    print("-" * 10 + "Week" + "-" * 10)
    need = 40
    have = 0
    today = dt.date.today()
    start_date = today - dt.timedelta(days=today.weekday())
    for interval in Interval.select():
        if interval.start.date() >= start_date:
            have += interval.duration / 60 / 60
    have = round(have * 100) / 100
    if have == 0:
        print("have/need:", f"{have}/{need}={round(0)*100}")
    else:
        print("have/need:", f"{have}/{need}={round((have/need)*10000)/100}%")
    print("last", f"{need}-{have}={need-have}")
    print("-" * 10 + "Day" + "-" * 10)
    today = dt.date.today()
    if today.weekday() >= 5:
        need = 0
    else:
        need = 8
    have = 0
    for interval in Interval.select():
        if interval.start.date() >= today:
            have += interval.duration / 60 / 60
    have = round(have * 100) / 100
    if have == 0:
        print("have/need:", f"{have}/{need}={round(0)*100}")
    else:
        print("have/need:", f"{have}/{need}={round((have/need)*10000)/100}%")
    print("last", f"{need}-{have}={need-have}")