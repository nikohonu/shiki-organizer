import datetime as dt
import math

from shiki_organizer.model import Interval, Task


def diff(a, b):
    result = ""
    flag = False
    for c_a, c_b in zip(a, b):
        if c_a != c_b:
            flag = True
        if flag:
            result += c_b
    return result


def get_status(message="Tracking") -> str:
    interval = Interval.select().order_by(Interval.start.desc()).get()
    task = interval.task
    end = interval.end if interval.end else dt.datetime.now()
    duration = str(
        dt.timedelta(seconds=math.floor((end - interval.start).total_seconds()))
    ).rjust(21, " ")
    start = interval.start.strftime("%Y-%m-%dT%H:%M:%S").rjust(19, " ")
    end = diff(start, end.strftime("%Y-%m-%dT%H:%M:%S")).rjust(19, " ")
    return f'{message} "{task.name}"\n  Started {interval.start}\n  Current {end}\n  Total {duration}'
