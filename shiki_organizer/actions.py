import datetime as dt

from shiki_organizer.model import Interval, Task


def stop() -> Task:
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        interval.end = dt.datetime.now()
        interval.save()
    return interval.task


def get_status(message: str = "Current task is", show_end=False) -> str:
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        task = interval.task
        end = f"\nEnd: {dt.datetime.strftime(dt.datetime.now(), '%X')}." if show_end else ""
        return f"{message} \"{task.name}\".\nStart: {dt.datetime.strftime(interval.start, '%X')}.{end}\nDuration: {dt.timedelta(seconds=round(interval.duration))}."
    else:
        return "Tasks are not currently being tracked."