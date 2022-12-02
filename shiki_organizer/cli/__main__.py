import datetime as dt
import math
import uuid

import click
from colorama import Fore, Style
from termcolor import colored

from shiki_organizer.actions import get_status
from shiki_organizer.model import Interval, Task


@click.group()
def cli():
    pass


@click.command()
@click.argument("name")
@click.option(
    "-p", "--priority", default=0, help="Priority of the task.", type=click.IntRange(0)
)
@click.option(
    "-i",
    "--divider",
    default=1,
    help="Divider of the task score.",
    type=click.IntRange(0),
)
@click.option(
    "-r",
    "--recurrence",
    is_flag=False,
    flag_value=1,
    help="Recurrence interval of the task.",
    type=click.IntRange(1),
)
@click.option(
    "-s",
    "--scheduled",
    is_flag=False,
    flag_value=str(dt.date.today()),
    help="Date when you plan to start working on this task.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "-d",
    "--deadline",
    is_flag=False,
    flag_value=str(dt.date.today()),
    help="Date when you plan to complete the work on this task.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "-a",
    "--parent",
    help="Id or uuid of the parent task.",
    type=str,
)
def add(name, priority, divider, recurrence, scheduled, deadline, parent):
    if parent:
        if parent.isnumeric():
            parent = Task.get_by_id(int(parent))
        else:
            parent = uuid.UUID(parent)
    task = Task.create(
        name=name,
        priority=priority,
        divider=divider,
        recurrence=recurrence,
        scheduled=scheduled.date() if scheduled else None,
        deadline=deadline.date() if deadline else None,
        parent=parent,
    )
    Task.reindex()
    task = Task.get_by_uuid(task.uuid)
    print(f"Created task {task.id}.")


@click.command()
@click.argument("task")
@click.option("-n", "--name", help="Name of a task.")
@click.option(
    "-p",
    "--priority",
    is_flag=False,
    flag_value=0,
    help="Priority of the task.",
    type=click.IntRange(0),
)
@click.option(
    "-i",
    "--divider",
    is_flag=False,
    flag_value=1,
    default=1,
    help="Divider of the task score.",
    type=click.IntRange(0),
)
@click.option(
    "-r",
    "--recurrence",
    is_flag=False,
    flag_value=0,
    help="Recurrence interval of the task.",
    type=click.IntRange(0),
)
@click.option(
    "-s",
    "--scheduled",
    is_flag=False,
    flag_value="0001-01-01",
    help="Date when you plan to start working on this task.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "-d",
    "--deadline",
    is_flag=False,
    flag_value="0001-01-01",
    help="Date when you plan to complete the work on this task.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "-a",
    "--parent",
    is_flag=False,
    flag_value="",
    help="Id or uuid of the parent task.",
    type=str,
)
def modify(task, name, priority, divider, recurrence, scheduled, deadline, parent):
    if task.isnumeric():
        task = Task.get_by_id(int(task))
    else:
        task = Task.get_by_uuid(uuid.UUID(task))
    name = task.name if name == None else name
    priority = task.priority if priority == None else priority
    divider = task.divider if divider == None else divider
    if recurrence == 0:
        recurrence = None
    elif recurrence == None:
        recurrence = task.recurrence
    else:
        recurrence
    if scheduled == dt.date.min:
        scheduled = None
    elif scheduled == None:
        scheduled = task.scheduled
    else:
        scheduled.date()
    if deadline == dt.date.min:
        deadline = None
    elif deadline == None:
        deadline = task.deadline
    else:
        deadline.date()
    if parent == "":
        parent = None
    elif parent == None:
        parent = task.parent
    else:
        if parent.isnumeric():
            parent = Task.get_by_id(int(parent))
        else:
            parent = uuid.UUID(parent)
    q = task.update(
        name=name,
        priority=priority,
        divider=divider,
        recurrence=recurrence,
        scheduled=scheduled,
        deadline=deadline,
        parent=parent,
    ).where(Task.id == task.id)
    q.execute()
    print(f"Modifying task {task.id} '{task.name}'.")


@click.command()
@click.option("-t", "--task", type=str, help="Id or uuid of the task")
@click.option("-d", "--description", type=str, help="Іnterval description")
@click.option(
    "-s",
    "--start",
    type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%S"]),
    default=dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    help="Start of the interval",
)
@click.option(
    "-e",
    "--end",
    type=click.DateTime(formats=["%Y-%m-%dT%H:%M:%S"]),
    help="End of the interval",
)
def start(task, description, start, end):
    if task.isnumeric():
        task = Task.get_by_id(int(task))
    else:
        task = Task.get_by_uuid(uuid.UUID(task))
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        if interval.task == task:
            print(get_status())
            return
        else:
            now = dt.datetime.now()
            interval.end = dt.datetime(
                now.year, now.month, now.day, now.hour, now.minute, now.second
            )
            interval.save()
            print(get_status("Recorded"))
    if end and end < start:
        end = None
        print("The end of the interval must be after the start.")
        return
    Interval.create(task=task, start=start, end=end, description=description)
    print(get_status())
    Interval.reindex()


@click.command()
def stop():
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        print(get_status("Recorded"))
        interval.end = dt.datetime.now()
        interval.save()
    else:
        print("There is no active time tracking.")


@click.command()
@click.option("-s", "--hide-scheduled", type=bool, help="ide tasks with scheduled")
@click.option(
    "-t/-n", "--today/--no-today", default=False, help="Show only today tasks"
)
def tree(today, hide_scheduled):
    def row_to_str(key, row):
        if row["task"].divider != 1:
            divider = f'({row["task"].divider}) '
        else:
            divider = ""
        if row["task"].priority != 0:
            priority = f'({row["task"].priority}) '
        else:
            priority = ""
        scheduled = row["task"].scheduled
        scheduled = (
            colored(f" scheduled:", "magenta") + str(scheduled) if scheduled else ""
        )
        deadline = row["task"].deadline
        deadline = colored(f" deadline:", "red") + str(deadline) if deadline else ""
        recurrence = row["task"].recurrence
        recurrence = (
            colored(f" recurrence:", "yellow") + str(recurrence) + "d"
            if recurrence
            else ""
        )
        duration = colored(f" duration:", "green") + f"{round(row['duration']/60)}"
        days = colored(f" days:", "blue") + f"{row['days']}"
        avg = colored(f" avg:", "cyan") + f"{round(row['avg']/60)}"
        score = colored(f" score:", "yellow") + f"{round(row['score']/60)}"
        return f'{divider}{priority}{key} {row["task"].name}{scheduled}{recurrence}{deadline}{duration}{days}{avg}{score}'

    def sort_queue(queue):
        if hide_scheduled:
            queue = list(filter(lambda x: table[x[1]]["task"].scheduled == None, queue))
        for x in queue:
            task = table[x[1]]["task"]
            if task.divider != 0:
                table[x[1]]["score"] = table[x[1]]["duration"] / task.divider
            else:
                table[x[1]]["score"] = -1
        if today:
            queue = sorted(
                queue,
                key=lambda x: table[x[1]]["task"].priority
                if table[x[1]]["task"].priority != 0
                else float("infinity"),
                reverse=True,
            )
        else:
            queue = sorted(queue, key=lambda x: table[x[1]]["score"], reverse=True)
            queue = list(filter(lambda x: table[x[1]]["score"] != -1, queue))
        return queue

    table = {}
    for task in Task.select():
        table[task.id] = {
            "task": task,
            "duration": 0,
            "days": set(),
            "avg": 0,
            "score": 0,
        }
    for interval in Interval.select():
        duration = interval.duration
        date = str(interval.start.date())
        for task in interval.task.parents + [interval.task]:
            if task.id in table:
                table[task.id]["days"].add(date)
                table[task.id]["duration"] += duration
    for key in table:
        table[key]["days"] = len(table[key]["days"])
        if table[key]["days"]:
            table[key]["avg"] = table[key]["duration"] / table[key]["days"]
        else:
            table[key]["avg"] = 0
    table = dict(sorted(table.items(), key=lambda tag: tag[1]["score"]))
    if today:
        table = dict(
            sorted(
                table.items(),
                key=lambda tag: tag[1]["task"].scheduled
                if tag[1]["task"].scheduled != None
                else dt.date.max,
            )
        )
        queue = [
            (0, task_id)
            for task_id in table
            if table[task_id]["task"].scheduled == dt.date.today()
        ]
    else:
        queue = [
            (0, task_id) for task_id in table if table[task_id]["task"].parent == None
        ]
    queue = sort_queue(queue)
    while queue:
        row = queue.pop()
        children = [(row[0] + 1, t.id) for t in table[row[1]]["task"].direct_children]
        children = sort_queue(children)
        queue += children
        if table[row[1]]["task"].archived == False:
            print(" " * 4 * row[0], row_to_str(row[1], table[row[1]]), sep="")


@click.command()
@click.argument("task")
def delete(task):
    if task.isnumeric():
        task = Task.get_by_id(int(task))
    else:
        task = Task.get_by_uuid(uuid.UUID(task))
    task.delete_instance()
    print(f"Deleting task {task.id} '{task.name}'.")
    Task.reindex()


@click.command()
def normalize():
    parents = {None: 1}
    count = 0

    for parent in Task.select():
        if Task.select().where(Task.parent == parent).count() > 2:
            parents[parent] = 1
    for parent in parents:
        tasks = Task.select().where(Task.parent == parent)
        divider = [task.divider for task in tasks]
        gcd = math.gcd(*divider)
        if gcd > 1:
            for task in tasks:
                task.divider /= gcd
            Task.bulk_update(tasks, [Task.divider])
            count += len(tasks)
    print(f"Modified {count} tasks.")


@click.command()
def status():
    if Interval.get_or_none(Interval.end == None):
        print(get_status())
    else:
        print("There is no active time tracking.")


@click.command()
@click.argument("task")
def done(task):
    if task.isnumeric():
        task = Task.get_by_id(int(task))
    else:
        task = Task.get_by_uuid(uuid.UUID(task))
    interval = Interval.get_or_none((Interval.end == None) & (Interval.task == task))
    if interval:
        print(get_status("Recorded"))
        interval.end = dt.datetime.now()
        interval.save()
    if task.recurrence:
        task.scheduled = (dt.datetime.now() + dt.timedelta(days=task.recurrence)).date()
        if task.deadline and task.scheduled > task.deadline:
            task.archived = True
            task.scheduled = dt.datetime.now()
    else:
        task.archived = True
    task.save()
    print(f"Completed task {task.id} '{task.name}'.")


@click.command()
@click.option("-u/-n", "--uuid/--no-uuid", default=False, help="Show only today tasks")
def interval_list(uuid):
    for interval in Interval.select():
        if uuid:
            uuid = f"{Fore.CYAN}uuid:{Style.RESET_ALL}{interval.uuid} "
        else:
            uuid = ""
        id = f"{Fore.RED}id:{Style.RESET_ALL}{interval.id} "
        if interval.task:
            task = f"{Fore.YELLOW}task:{Style.RESET_ALL}'{interval.task.name}' "
        else:
            task = ""
        if interval.description:
            description = (
                f"{Fore.GREEN}description:{Style.RESET_ALL}{interval.description} "
            )
        else:
            description = ""
        start = f"{Fore.BLUE}start:{Style.RESET_ALL}'{interval.start}' "
        if interval.end:
            end = f"{Fore.MAGENTA}end:{Style.RESET_ALL}'{interval.end}'"
        else:
            end = ""
        print(f"{uuid}{id}{task}{description}{start}{end}")


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
    "-d",
    "--description",
    is_flag=False,
    flag_value="",
    help="Description of interval.",
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
def modify_interval(interval, task, description, start, end):
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
    if description == None:
        description = interval.description
    elif description == "":
        description = None
    if start == None:
        start = interval.start
    if end == None:
        end = interval.end
    elif end == dt.datetime.min:
        end = None
    q = interval.update(
        task=task,
        description=description,
        start=start,
        end=end,
    ).where(Interval.id == interval.id)
    q.execute()
    print(f"Modifying interval {interval.id}'.")


@click.command()
@click.argument("interval")
def delete_interval(interval):
    if interval.isnumeric():
        interval = Interval.get_by_id(int(interval))
    else:
        interval = Interval.get_by_uuid(uuid.UUID(interval))
    interval.delete_instance()
    print(f"Deleting interval {interval.id}.")
    Interval.reindex()


cli.add_command(add)
cli.add_command(modify)
cli.add_command(start)
cli.add_command(stop)
cli.add_command(tree)
cli.add_command(delete)
cli.add_command(normalize)
cli.add_command(status)
cli.add_command(done)
cli.add_command(interval_list)
cli.add_command(modify_interval)
cli.add_command(delete_interval)


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
