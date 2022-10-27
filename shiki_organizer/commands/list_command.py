import argparse
import datetime as dt

from termcolor import colored

from shiki_organizer.model import Field, Interval, Task


def list_subparsers(subparsers: argparse._SubParsersAction):
    parser_list: argparse.ArgumentParser = subparsers.add_parser(
        "list", help="show tasks"
    )
    parser_list.add_argument(
        "-t",
        "--today",
        action="store_true",
        help="show today task",
    )


def tree_subparsers(subparsers: argparse._SubParsersAction):
    parser_list: argparse.ArgumentParser = subparsers.add_parser(
        "tree", help="show tree"
    )
    parser_list.add_argument(
        "-i",
        "--interval",
        help="show stats based on interval",
        choices=["week", "month", "quarter", "year", "all"],
        default="all",
    )


def run_list_command(args: argparse.Namespace, parser: argparse.ArgumentParser):
    sorted_task = sorted(
        Task.select(),
        key=lambda x: x.scheduled if x.scheduled != None else dt.date.max,
    )
    for task in sorted_task:
        if vars(args).get("today") and args.today and task.scheduled != dt.date.today():
            continue
        if task.is_completed:
            continue
        scheduled = (
            colored(f" scheduled:", "red") + f"{task.scheduled}"
            if task.scheduled
            else ""
        )
        deadline = (
            colored(f" deadline:", "green") + f"{task.deadline}"
            if task.deadline
            else ""
        )
        recurrence = (
            colored(f" recurrence:", "yellow") + f"{task.recurrence}{task.unit}"
            if task.recurrence
            else ""
        )
        days = colored(f" days:", "blue") + f"{task.days}"
        duration = colored(f" duration:", "magenta") + f"{round(task.duration/60)}"
        avg = (
            colored(f" avg:", "cyan") + f"{round(task.duration/task.days/60)}"
            if task.days > 0
            else ""
        )
        print(
            f"{task.id}. {task.description}{scheduled}{deadline}{recurrence}{days}{duration}{avg}"
        )


def get_children(table, parent):
    rows = []
    for key in table:
        if table[key]["parent"] == parent and not table[key]["is_hidden"]:
            rows.append(key)
    rows.reverse()
    return rows


def row_to_str(key, row):
    id = f"{key}. " if key.isnumeric() else ""
    divider = f'({row["divider"]}) '
    duration = colored(f" duration:", "green") + f"{round(row['duration']/60)}"
    days = colored(f" days:", "blue") + f"{row['days']}"
    avg = colored(f" avg:", "cyan") + f"{round(row['avg']/60)}"
    score = colored(f" score:", "yellow") + f"{round(row['score']/60)}"
    return f'{id}{divider}{row["name"]}{duration}{days}{avg}{score}'


def get_divider(model, interval):
    match interval:
        case "year":
            return model.year_divider
        case "quarter":
            return model.quarter_divider
        case "month":
            return model.month_divider
        case "week":
            return model.week_divider
        case _:
            return model.divider


def get_start_datetime(interval: str):
    today = dt.date.today()
    match interval:
        case "year":
            epoch_year = dt.date.today().year
            return dt.date(epoch_year, 1, 1)
        case "quarter":
            return dt.date(today.year, 3 * ((today.month - 1) // 3) + 1, 1)
        case "month":
            epoch_year = dt.date.today().year
            epoch_month = dt.date.today().month
            return dt.date(epoch_year, epoch_month, 1)
        case "week":
            return today - dt.timedelta(days=today.weekday())
        case _:
            return dt.date.min


def run_tree_command(args: argparse.Namespace, parser: argparse.ArgumentParser):
    start_date = get_start_datetime(args.interval)
    table = {}
    for field in Field.select():
        table["f" + str(field.id)] = {
            "name": field.name,
            "divider": get_divider(field, args.interval),
            "duration": 0,
            "days": set(),
            "avg": 0,
            "score": 0,
            "is_hidden": False,
            "parent": None,
        }
    for task in Task.select():
        parent_key = None
        if task.field != None:
            if not task.category:
                parent_key = "f" + str(task.field.id)
            else:
                category = task.category
                parent_key = "f" + str(task.field.id) + "c" + str(task.category.id)
                while category:
                    if category.category:
                        category_parent_key = (
                            "f" + str(task.field.id) + "c" + str(category.category.id)
                        )
                    else:
                        category_parent_key = "f" + str(task.field.id)
                    table["f" + str(task.field.id) + "c" + str(category.id)] = {
                        "name": category.name,
                        "divider": get_divider(field, args.interval),
                        "duration": 0,
                        "days": set(),
                        "avg": 0,
                        "score": 0,
                        "is_hidden": False,
                        "parent": category_parent_key,
                    }
                    category = category.category
        table[str(task.id)] = {
            "name": task.description,
            "divider": get_divider(task, args.interval),
            "duration": 0,
            "days": set(),
            "avg": 0,
            "score": 0,
            "is_hidden": task.is_hidden or task.is_completed,
            "parent": parent_key,
        }
    for interval in Interval.select():
        if interval.start.date() < start_date:
            continue
        duration = interval.duration
        date = str(interval.start.date())
        task = interval.task
        for key in table:
            check = False
            children = set()
            queue = get_children(table, key)
            while queue:
                child = queue.pop()
                queue += get_children(table, child)
                children.add(child)
            if key == str(task.id):
                check = True
            for child in children:
                if child == str(task.id):
                    check = True
            if check:
                table[key]["days"].add(date)
                table[key]["duration"] += duration
    for key in table:
        table[key]["days"] = len(table[key]["days"])
        if table[key]["days"]:
            table[key]["avg"] = table[key]["duration"] / table[key]["days"]
        else:
            table[key]["avg"] = 0
        table[key]["score"] = table[key]["duration"] / float(table[key]["divider"])
    table = dict(sorted(table.items(), key=lambda tag: tag[1]["score"]))
    queue = [
        (0, row)
        for row in table
        if table[row]["parent"] == None and not table[row]["is_hidden"]
    ]
    queue.reverse()
    while queue:
        row = queue.pop()
        children = [(row[0] + 1, t) for t in get_children(table, row[1])]
        queue += children
        print(" " * 4 * row[0], row_to_str(row[1], table[row[1]]), sep="")
