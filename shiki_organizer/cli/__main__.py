import datetime as dt
import string
import uuid

import click
from colorama import Fore, Style

from shiki_organizer.actions import get_status
from shiki_organizer.model import Interval, Project, Tag, Task


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
    "-d",
    "--deadline",
    is_flag=False,
    flag_value=str(dt.date.today()),
    help="Date when you plan to complete the work on this task.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "-t",
    "--tags",
    multiple=True,
    help="Tags of the task.",
    type=str,
)
@click.option(
    "--project",
    help="Project of the task.",
    type=str,
)
def add(description, priority, recurrence, scheduled, deadline, tags, project):
    project, _ = Project.get_or_create(name=project) if project else (None, None)
    tags = [tag for tag, _ in [Tag.get_or_create(name=tag) for tag in tags]]
    task = Task.create(
        description=description,
        priority=priority,
        recurrence=recurrence,
        scheduled=scheduled.date() if scheduled else None,
        deadline=deadline.date() if deadline else None,
        project=project,
    )
    task.tags.add(tags)
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
    "-d",
    "--deadline",
    is_flag=False,
    flag_value="0001-01-01",
    help="Date when you plan to complete the work on this task.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option(
    "-t",
    "--tags",
    is_flag=False,
    flag_value="",
    multiple=True,
    help="Tags of the task.",
    type=str,
)
@click.option(
    "--project",
    is_flag=False,
    flag_value="",
    help="Project of the task.",
    type=str,
)
def modify(task, description, priority, recurrence, scheduled, deadline, tags, project):
    if task.isnumeric():
        task = Task.get_by_id(int(task))
    else:
        task = Task.get_by_uuid(uuid.UUID(task))
    description = task.description if description == None else description
    if priority == None:
        priority = task.priority
    elif priority == "":
        priority = None
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
    if len(tags) == 0:
        pass
    elif len(tags) == 1 and tags[0] == "":
        task.tags.clear()
    else:
        task.tags.clear()
        tags = [tag for tag, _ in [Tag.get_or_create(name=tag) for tag in tags]]
        task.tags.add(tags)
    if project == None:
        project = task.project
    elif project == "":
        project = None
    else:
        project, _ = Project.get_or_create(name=project)
    q = task.update(
        description=description,
        priority=priority,
        recurrence=recurrence,
        scheduled=scheduled,
        deadline=deadline,
        project=project,
    ).where(Task.id == task.id)
    q.execute()
    Project.remove_unused()
    Tag.remove_unused()
    print(f"Modifying task {task.id} '{task.description}'.")


@click.command()
@click.argument("task")
def delete(task):
    if task.isnumeric():
        task = Task.get_by_id(int(task))
    else:
        task = Task.get_by_uuid(uuid.UUID(task))
    task.tags.clear()
    Interval.delete().where(Interval.task == task).execute()
    task.delete_instance()
    Project.remove_unused()
    Tag.remove_unused()
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
    print(f"Completed task {task.id} '{task.description}'.")


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
            task = f"{Fore.YELLOW}task:{Style.RESET_ALL}'{interval.task.description}' "
        else:
            task = ""
        start = f"{Fore.BLUE}start:{Style.RESET_ALL}'{interval.start}' "
        if interval.end:
            end = f"{Fore.MAGENTA}end:{Style.RESET_ALL}'{interval.end}'"
        else:
            end = ""
        print(f"{uuid}{id}{task}{start}{end}")


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
def interval_modify(interval, task, start, end):
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
def interval_delete(interval):
    if interval.isnumeric():
        interval = Interval.get_by_id(int(interval))
    else:
        interval = Interval.get_by_uuid(uuid.UUID(interval))
    interval.delete_instance()
    print(f"Deleting interval {interval.id}.")
    Interval.reindex()


@click.command(name="ls")
@click.option(
    "-t", "--today", is_flag=True, default=False, help="Show only today tasks."
)
@click.option(
    "-p",
    "--project",
    is_flag=False,
    flag_value="",
    type=str,
    help="Filter tasks by project.",
)
@click.option(
    "--tag", type=str, is_flag=False, flag_value="", help="Filter tasks by tag."
)
def ls(today, project, tag):
    def task_to_str(task):
        if task.priority:
            priority = f"{Fore.BLUE}({task.priority}){Style.RESET_ALL} "
        else:
            priority = ""
        scheduled = (
            f" {Fore.MAGENTA}scheduled:{Style.RESET_ALL}" + str(task.scheduled)
            if task.scheduled
            else ""
        )
        deadline = (
            f" {Fore.RED}deadline:{Style.RESET_ALL}" + str(task.deadline)
            if task.deadline
            else ""
        )
        recurrence = (
            f" {Fore.YELLOW}recurrence:{Style.RESET_ALL}{task.recurrence}d"
            if task.recurrence
            else ""
        )
        project = (
            f" {Fore.CYAN}project:{Style.RESET_ALL}{task.project.name}"
            if task.project
            else ""
        )
        tags = (
            " ".join([f"{Fore.GREEN}+{tag.name}{Style.RESET_ALL}" for tag in task.tags])
            if task.tags
            else ""
        )
        return f"{task.id} {priority}{task.description}{scheduled}{recurrence}{deadline}{project} {tags}"

    tasks = None
    if project:
        tasks = Task.select().join(Project).where(Project.name == project)
    if project == "":
        tasks = Task.select().where(Task.project == None)
    if tag != None:
        tag = None if not tag else tag
        tasks = []
        for task in Task.select():
            tag_nams = [tag.name for tag in task.tags]
            if tag:
                if tag in tag_nams:
                    tasks.append(task)
            elif len(tag_nams) == 0:
                tasks.append(task)
    if not tasks:
        tasks = Task.select()
    if today:
        tasks = tasks.where(Task.scheduled == dt.date.today())
    tasks = sorted(tasks, key=lambda x: x.priority if x.priority else "a")
    tasks = sorted(tasks, key=lambda x: x.scheduled if x.scheduled else dt.date.max)
    for task in tasks:
        print(task_to_str(task))


@click.command()
def tags():
    tags = {}
    global_duration = 0
    for interval in Interval.select():
        for tag in interval.task.tags:
            duration = interval.duration
            if tag in tags:
                tags[tag] += duration
            else:
                tags[tag] = duration
            global_duration += duration
    tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)
    for tag, duration in tags:
        print(
            tag.name,
            round(duration / 60 * 100) / 100,
            f"{round(duration / global_duration * 10000)/100}%",
        )


@click.command()
def projects():
    projects = {}
    global_duration = 0
    for interval in Interval.select():
        duration = interval.duration
        project = interval.task.project
        if project:
            if project in projects:
                projects[project] += duration
            else:
                projects[project] = duration
            global_duration += duration
    projects = sorted(projects.items(), key=lambda x: x[1], reverse=True)
    for project, duration in projects:
        print(
            project.name,
            round(duration / 60 * 100) / 100,
            f"{round(duration / global_duration * 10000)/100}%",
        )


@click.command()
def today():
    global_duration = 0
    for interval in Interval.select():
        if interval.start.date() == dt.date.today():
            global_duration += interval.duration
    print(f"{round(global_duration / 60 / 60 * 100) / 100}h")


cli.add_command(add)
cli.add_command(modify)
cli.add_command(delete)
cli.add_command(start)
cli.add_command(stop)
cli.add_command(status)
cli.add_command(done)
cli.add_command(interval_list)
cli.add_command(interval_modify)
cli.add_command(interval_delete)
cli.add_command(ls)
cli.add_command(tags)
cli.add_command(projects)
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
