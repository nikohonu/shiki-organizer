import datetime as dt
import os
import string
import uuid

import click
from colorama import Fore, Style
from github import Github

from shiki_organizer.actions import get_status
from shiki_organizer.model import Interval, Issue, Task


@click.group()
def cli():
    pass


@click.command()
@click.argument("description")
@click.option(
    "-p",
    "--priority",
    help="Priority of the task.",
    type=click.Choice(list(string.ascii_uppercase)),
)
@click.option(
    "-d",
    "--divider",
    default=1,
    help="Divider of the task.",
    type=click.IntRange(1),
)
@click.option(
    "-r",
    "--recurrence",
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
    "--deadline",
    is_flag=False,
    flag_value=str(dt.date.today()),
    help="Date when you plan to complete the work on this task.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "--parent",
    help="Id or uuid of the parent task.",
    type=str,
)
def add(description, priority, divider, recurrence, scheduled, deadline, parent):
    if parent:
        if parent.isnumeric():
            parent = Task.get_by_id(int(parent))
        else:
            parent = uuid.UUID(parent)
    task = Task.create(
        description=description,
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
@click.option(
    "-n",
    "--description",
    help="Description of the task.",
    type=str,
)
@click.option(
    "-p",
    "--priority",
    is_flag=False,
    flag_value="",
    help="Priority of the task.",
    type=click.Choice(list(string.ascii_uppercase) + [""]),
)
@click.option(
    "-d",
    "--divider",
    is_flag=False,
    flag_value=1,
    help="Divider of the task.",
    type=click.IntRange(1),
)
@click.option(
    "-r",
    "--recurrence",
    is_flag=False,
    flag_value=0,
    help="Recurrence interval of the task.",
    type=int,
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
    "--deadline",
    is_flag=False,
    flag_value="0001-01-01",
    help="Date when you plan to complete the work on this task.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "--parent",
    is_flag=False,
    flag_value="",
    help="Id or uuid of the parent task.",
    type=str,
)
def modify(
    task, description, priority, divider, recurrence, scheduled, deadline, parent
):
    if task.isnumeric():
        task = Task.get_by_id(int(task))
    else:
        task = Task.get_by_uuid(uuid.UUID(task))
    if parent:
        if parent.isnumeric():
            parent = Task.get_by_id(int(parent))
        else:
            parent = uuid.UUID(parent)
    elif parent == "":
        parent = None
    else:
        parent = task.parent

    description = task.description if description == None else description
    if priority == None:
        priority = task.priority
    elif priority == "":
        priority = None
    if divider == None:
        divider = task.divider
    if recurrence == None:
        recurrence = task.recurrence
    elif recurrence == 0:
        recurrence = None
    if scheduled == None:
        scheduled = task.scheduled
    elif scheduled == dt.datetime.min:
        scheduled = None
    else:
        scheduled = scheduled.date()
    if deadline == None:
        deadline = task.deadline
    elif deadline == dt.datetime.min:
        deadline = None
    else:
        deadline = deadline.date()
    q = task.update(
        description=description,
        priority=priority,
        divider=divider,
        recurrence=recurrence,
        scheduled=scheduled,
        deadline=deadline,
        parent=parent,
    ).where(Task.id == task.id)
    q.execute()
    print(f"Modifying task {task.id} '{task.description}'.")


@click.command()
@click.argument("task")
def delete(task):
    if task.isnumeric():
        task = Task.get_by_id(int(task))
    else:
        task = Task.get_by_uuid(uuid.UUID(task))
    Interval.delete().where(Interval.task == task).execute()
    task.delete_instance()
    print(f"Deleting task {task.id} '{task.description}'.")


@click.command()
@click.argument("task")
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
def start(task, start, end):
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
    Interval.create(task=task, start=start, end=end)
    print(get_status())
    Interval.reindex()


@click.command()
def stop():
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        print(get_status("Recorded"))
        now = dt.datetime.now()
        interval.end = dt.datetime(
            now.year, now.month, now.day, now.hour, now.minute, now.second
        )
        interval.save()
    else:
        print("There is no active time tracking.")


@click.command()
def status():
    if Interval.get_or_none(Interval.end == None):
        print(get_status())
    else:
        print("There is no active time tracking.")


@click.command()
@click.argument("task")
@click.option("--github-token", default=lambda: os.environ.get("GITHUB_TOKEN", ""))
def done(task, github_token):
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
    print(f"Completed task {task.id} '{task.description}'.")
    issue = Issue.get_or_none(Issue.task == task)
    if issue:
        if not github_token:
            print("GitHub token is required.")
            return
        g = Github(github_token)
        repo = g.get_repo(issue.repository.name)
        open_issues = repo.get_issues(state="open")
        for i in open_issues:
            if issue.id == i.number:
                i.edit(state="closed")
        print(f"Close issue {task.id} '{task.description}'.")


# def update(task: Task):
def update():
    query = Task.update(duration=0)
    query.execute()
    intervals = Interval.select()
    items = {}
    for interval in intervals:
        task = interval.task
        while task:
            if task.id not in items:
                items[task.id] = {"task": task, "duration": 0, "days": 0}
                items[task.id]["duration"] = interval.duration
                items[task.id]["today_duration"] = 0
                if interval.start.date() == dt.date.today():
                    items[task.id]["today_duration"] = interval.duration
                items[task.id]["days"] = set([interval.start.date()])
            else:
                items[task.id]["duration"] += interval.duration
                if interval.start.date() == dt.date.today():
                    items[task.id]["today_duration"] += interval.duration
                items[task.id]["days"].add(interval.start.date())
            task = task.parent
    tasks = []
    for item in items:
        task = items[item]["task"]
        task.days = len(items[item]["days"])
        task.duration = items[item]["duration"]
        task.today_duration = items[item]["today_duration"]
        tasks.append(task)
    Task.bulk_update(tasks, fields=[Task.duration, Task.today_duration, Task.days])


def task_to_str(task):
    def get_value(value, name, color):
        return f" {color}{name}:{Style.RESET_ALL}" + str(value) if value else ""

    id = task.id if task.id else f"uuid:{task.uuid}"
    if task.priority:
        priority = f"{Fore.BLUE}({task.priority}){Style.RESET_ALL} "
    else:
        priority = ""
    if task.divider > 1:
        divider = f"{Fore.RED}({task.divider}){Style.RESET_ALL} "
    else:
        divider = ""
    scheduled = get_value(task.scheduled, "scheduled", Fore.MAGENTA)
    deadline = get_value(task.deadline, "deadline", Fore.RED)
    recurrence = (
        f" {Fore.YELLOW}recurrence:{Style.RESET_ALL}{task.recurrence}d"
        if task.recurrence
        else ""
    )
    duration = get_value(int(task.duration / 60), "duration", Fore.GREEN)
    today_duration = get_value(
        int(task.today_duration / 60), "t-duration", Fore.MAGENTA
    )
    days = get_value(task.days, "days", Fore.BLUE)
    score = get_value(int(task.score / 60), "score", Fore.RED)
    today_score = get_value(int(task.today_duration / 60), "t-score", Fore.RED)
    average = get_value(int(task.average / 60), "average", Fore.CYAN)
    return f"{id} {priority}{divider}{task.description}{scheduled}{recurrence}{deadline}{duration}{today_duration}{days}{average}{score}{today_score}"


@click.command(name="ls")
@click.option(
    "-t", "--today", is_flag=True, default=False, help="Show only today tasks."
)
@click.option(
    "-a", "--archived", is_flag=True, default=False, help="Show archived task."
)
def ls(today, archived):

    tasks = None
    if not tasks:
        tasks = Task.select()
    if today:
        tasks = tasks.where(Task.scheduled == dt.date.today())
        tasks = sorted(tasks, key=lambda x: x.priority if x.priority else "a")
        tasks = sorted(tasks, key=lambda x: x.scheduled if x.scheduled else dt.date.max)
    else:
        tasks = sorted(Task.select(), key=lambda x: x.score)

    if not archived:
        tasks = filter(lambda x: not x.archived, tasks)
    for task in tasks:
        print(task_to_str(task))


@click.command()
def today():
    global_duration = 0
    for interval in Interval.select():
        if interval.start.date() == dt.date.today():
            global_duration += interval.duration
    print(f"{round(global_duration / 60 / 60 * 100) / 100}h")


@click.command()
@click.option(
    "-t", "--today", is_flag=True, default=False, help="Show only today tasks."
)
def tree(today):
    update()
    reverse = False
    if today:
        tasks = sorted(
            Task.select().where(Task.parent == None),
            key=lambda x: x.today_score,
            reverse=reverse,
        )
    else:
        tasks = sorted(
            Task.select().where(Task.parent == None),
            key=lambda x: x.score,
            reverse=reverse,
        )
    queue = [(0, task) for task in tasks]
    while queue:
        item = queue.pop()
        if not item[1].archived:
            if today:
                tasks = sorted(
                    Task.select().where(Task.parent == item[1]),
                    key=lambda x: x.today_score,
                    reverse=reverse,
                )
            else:
                tasks = sorted(
                    Task.select().where(Task.parent == item[1]),
                    key=lambda x: x.score,
                    reverse=reverse,
                )
            queue += [(item[0] + 1, task) for task in tasks]
            space = "\t"
            print(f"{space * item[0]}{task_to_str(item[1])}")


cli.add_command(add)
cli.add_command(modify)
cli.add_command(delete)
cli.add_command(start)
cli.add_command(stop)
cli.add_command(status)
cli.add_command(done)
cli.add_command(ls)
cli.add_command(tree)
cli.add_command(today)


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
