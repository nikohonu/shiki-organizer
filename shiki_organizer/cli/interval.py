import datetime as dt
import uuid

import click

from shiki_organizer.model import Interval, Task
from shiki_organizer.formatting import duration_to_str, interval_to_str
import pendulum
from colorama import Fore, Style


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "-u", "--uuid", is_flag=True, default=False, help="Show uuid of interval."
)
@click.option(
    "-p",
    "--period",
    type=click.Choice(["all", "today", "week", "month", "year"]),
    default="all",
    help="Show data only for this period of time.",
)
def ls(uuid, period):
    start = pendulum.now()
    match period:
        case "today":
            start = start.start_of("day")
        case "week":
            start = start.start_of("week")
        case "month":
            start = start.start_of("month")
        case "year":
            start = start.start_of("year")
        case _:
            start = dt.datetime.min
    if start != dt.datetime.min:
        start_string = start.to_datetime_string()
        start = dt.datetime.fromisoformat(start_string)
    intervals = Interval.select().where(Interval.start >= start)
    total_duration = 0
    for interval in intervals:
        total_duration += interval.duration
        print(interval_to_str(interval, uuid))
    print(
        f"{Fore.MAGENTA}Total duration:{Style.RESET_ALL}{duration_to_str(total_duration)}"
    )


@click.command()
@click.argument("interval")
@click.option(
    "-t",
    "--task",
    is_flag=False,
    flag_value="",
    help="Id or uuid of the parent task.",
    type=str,
)
@click.option(
    "-s",
    "--start",
    type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%S"]),
    help="Start of the interval",
)
@click.option(
    "-e",
    "--end",
    is_flag=False,
    flag_value="0001-01-01T00:00:00",
    type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%S"]),
    help="End of the interval",
)
def modify(interval, task, start, end):
    if interval.isnumeric():
        interval = Interval.get_by_id(int(interval))
    else:
        interval = Interval.get_by_uuid(uuid.UUID(interval))
    if task == None:
        task = interval.task
    elif task == "":
        task = None
    else:
        if task.isnumeric():
            task = Task.get_by_id(int(task))
        else:
            task = Task.get_by_uuid(uuid.UUID(task))
    if start == None:
        start = interval.start
    if end == None:
        end = interval.end
    elif end == dt.datetime.min:
        end = None
    q = interval.update(
        task=task,
        start=start,
        end=end,
    ).where(Interval.id == interval.id)
    q.execute()
    print(f"Modifying interval {interval.id}'.")


@click.command()
@click.argument("interval")
def delete(interval):
    if interval.isnumeric():
        interval = Interval.get_by_id(int(interval))
    else:
        interval = Interval.get_by_uuid(uuid.UUID(interval))
    interval.delete_instance()
    print(f"Deleting interval {interval.id}.")
    Interval.reindex()


cli.add_command(ls)
cli.add_command(modify)
cli.add_command(delete)


def main():
    # processing
    for task in Task.select():
        if not task.archived and task.scheduled and task.scheduled < dt.date.today():
            task.scheduled = dt.date.today()
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
    cli()


if __name__ == "__main__":
    main()
