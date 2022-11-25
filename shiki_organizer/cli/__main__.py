import argparse
import datetime as dt

from peewee import Select
from termcolor import colored

from shiki_organizer.model import Interval, IntervalTask, Task, TaskTask


def str_to_date(date, name, parser):
    result = None
    if date:
        if date == "today":
            result = dt.date.today()
        else:
            try:
                result: dt.date = dt.datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                parser.error(
                    f"the format of the {name} is incorrect. Try this: YYYY-MM-DD"
                )
    return result


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

    parser = argparse.ArgumentParser(description="To-do list.")
    subparsers = parser.add_subparsers(help="sub-command help", dest="command")
    task_ids = [t.id for t in Task.select()]
    # add
    add_parser = subparsers.add_parser("add", help="add task")
    add_parser.add_argument("name", help="name of the task")
    # edit
    edit_parser = subparsers.add_parser("edit", help="edit the task")
    edit_parser.add_argument(
        "id", help="id of the task", type=int, choices=[t.id for t in Task.select()]
    )
    edit_parser.add_argument("-n", "--name", help="name of the task")
    # edit & add
    for p in [add_parser, edit_parser]:
        p.add_argument(
            "-r", "--recurrence", help="set the recurrence interval", type=int
        )
        p.add_argument(
            "-s",
            "--scheduled",
            help="the date when you plan to start working on that task. Example: 2022-10-13",
        )

        p.add_argument(
            "-d",
            "--deadline",
            help="the date when you plan to finish working on that task. Example: 2022-10-23",
        )
        p.add_argument(
            "-t",
            "--tasks",
            nargs="+",
            help="ids of parent tasks",
            type=int,
            choices=task_ids,
        )
    # start
    start_parser: argparse.ArgumentParser = subparsers.add_parser(
        "start", help="start tasks"
    )
    start_parser.add_argument(
        "ids",
        help="ids of tasks",
        type=int,
        nargs="+",
        choices=task_ids,
    )
    # stop
    stop_parser: argparse.ArgumentParser = subparsers.add_parser(
        "stop", help="stop a task"
    )
    # del
    del_parser = subparsers.add_parser("del", help="delete tasks")
    del_parser.add_argument(
        "ids",
        help="ids of tasks",
        type=int,
        nargs="+",
        choices=task_ids,
    )
    # done
    done_parser = subparsers.add_parser("done", help="complete tasks")
    done_parser.add_argument(
        "ids",
        help="ids of tasks",
        type=int,
        nargs="+",
        choices=task_ids,
    )
    # tree
    tree_parser = subparsers.add_parser("tree", help="print tasks as tree")
    tree_parser.add_argument(
        "-t",
        "--today",
        help="show only today tasks",
        action="store_true",
    )

    # ...
    args = parser.parse_args()
    match args.command:
        case "add":
            scheduled = str_to_date(args.scheduled, "scheduled", parser)
            deadline = str_to_date(args.deadline, "deadline", parser)
            task = Task.create(
                name=args.name,
                recurrence=args.recurrence,
                scheduled=scheduled,
                deadline=deadline,
            )
            if args.tasks:
                for parent_id in args.tasks:
                    parent = Task.get_by_id(parent_id)
                    TaskTask.create(child=task, parent=parent)
        case "edit":
            scheduled = str_to_date(args.scheduled, "scheduled", parser)
            deadline = str_to_date(args.deadline, "deadline", parser)
            task = Task.get_by_id(args.id)
            task.name = args.name if args.name else task.name
            task.recurrence = args.recurrence if args.recurrence else task.recurrence
            task.scheduled = scheduled if scheduled else task.scheduled
            task.deadline = deadline if deadline else task.deadline
            task.save()
            if args.tasks:
                q = TaskTask.delete().where(TaskTask.child == task)
                q.execute()
                if args.tasks:
                    for parent_id in args.tasks:
                        parent = Task.get_by_id(parent_id)
                        TaskTask.create(child=task, parent=parent)
        case "start":
            tasks = set()
            root_tasks = Task.select().where(Task.id << args.ids)
            for task in root_tasks:
                tasks.add(task)
                parents = task.parents
                if parents:
                    tasks.update(parents)
            current_interval = Interval.get_or_none(Interval.end == None)
            if not current_interval:
                interval = Interval.create()
                for task in tasks:
                    IntervalTask.create(interval=interval, task=task)
            else:
                print("You need to stop the previous task before starting a new one.")
            names = " ".join([f'"{task.name}"' for task in root_tasks])
            print(f"Start {names}")
        case "stop":
            interval = Interval.get_or_none(Interval.end == None)
            if interval:
                interval.end = dt.datetime.now()
                interval.save()
        case "tree":

            def get_children(table, parent_id):
                rows = []
                children = [
                    tt.child
                    for tt in TaskTask.select(TaskTask.child).where(
                        TaskTask.parent == table[parent_id]["task"]
                    )
                ]
                for task_id in table:
                    if table[task_id]["task"] in children:
                        rows.append(task_id)
                rows.reverse()
                return rows

            def row_to_str(key, row):
                divider = f'({row["task"].divider}) '
                scheduled = row["task"].scheduled
                scheduled = (
                    colored(f" scheduled:", "magenta") + str(scheduled)
                    if scheduled
                    else ""
                )
                deadline = row["task"].deadline
                deadline = (
                    colored(f" deadline:", "red") + str(deadline) if deadline else ""
                )
                recurrence = row["task"].recurrence
                recurrence = (
                    colored(f" recurrence:", "yellow") + str(recurrence) + "d"
                    if recurrence
                    else ""
                )
                duration = (
                    colored(f" duration:", "green") + f"{round(row['duration']/60)}"
                )
                days = colored(f" days:", "blue") + f"{row['days']}"
                avg = colored(f" avg:", "cyan") + f"{round(row['avg']/60)}"
                score = colored(f" score:", "yellow") + f"{round(row['score']/60)}"
                return f'{divider}{key} {row["task"].name}{scheduled}{recurrence}{deadline}{duration}{days}{avg}{score}'

            table = {}
            for task in Task.select().where(Task.archived == False):
                table[task.id] = {
                    "task": task,
                    "duration": 0,
                    "days": set(),
                    "avg": 0,
                    "score": 0,
                    "parents": TaskTask.select().where(TaskTask.child == task).count(),
                }
            for interval in Interval.select():
                duration = interval.duration
                date = str(interval.start.date())
                tasks = set(
                    [
                        it.task
                        for it in IntervalTask.select().where(
                            IntervalTask.interval == interval
                        )
                    ]
                )
                for task in tasks:
                    table[task.id]["days"].add(date)
                    table[task.id]["duration"] += duration
            for key in table:
                table[key]["days"] = len(table[key]["days"])
                if table[key]["days"]:
                    table[key]["avg"] = table[key]["duration"] / table[key]["days"]
                else:
                    table[key]["avg"] = 0
                table[key]["score"] = table[key]["duration"] / float(
                    table[key]["task"].divider
                )
            table = dict(sorted(table.items(), key=lambda tag: tag[1]["score"]))
            if args.today:
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
                    (0, task_id) for task_id in table if table[task_id]["parents"] == 0
                ]
            queue.reverse()
            while queue:
                row = queue.pop()
                children = [(row[0] + 1, t) for t in get_children(table, row[1])]
                queue += children
                print(" " * 4 * row[0], row_to_str(row[1], table[row[1]]), sep="")

        case "del":
            tasks = Task.select().where(Task.id << args.ids)
            q = IntervalTask.delete().where(IntervalTask.task << tasks)
            q.execute()
            q = TaskTask.delete().where(TaskTask.child << tasks)
            q.execute()
            q = TaskTask.delete().where(TaskTask.parent << tasks)
            q.execute()
            interval_ids = set()
            for interval in Interval.select():
                if (
                    IntervalTask.select()
                    .where(IntervalTask.interval == interval)
                    .count()
                    == 0
                ):
                    interval_ids.add(interval.id)
            q = Interval.delete().where(Interval.id << interval_ids)
            q.execute()
            q = Task.delete().where(Task.id << [task.id for task in tasks])
            q.execute()

        case "done":
            tasks = Task.select().where(Task.id << args.ids)
            for task in tasks:
                if task.recurrence:
                    task.scheduled = (
                        dt.datetime.now() + dt.timedelta(days=task.recurrence)
                    ).date()
                    if task.deadline and task.scheduled > task.deadline:
                        task.archived = True
                        task.scheduled = dt.datetime.now()
                else:
                    task.archived = True
                task.save()
        case _:
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


if __name__ == "__main__":
    main()