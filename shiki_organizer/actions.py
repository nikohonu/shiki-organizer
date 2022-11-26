import datetime as dt

from shiki_organizer.model import Interval, Task


def stop() -> Task:
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        interval.end = dt.datetime.now()
        interval.save()
    return interval.task