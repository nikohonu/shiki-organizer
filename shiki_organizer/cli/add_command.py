import argparse
import datetime as dt

from shiki_organizer.model import Category, Field, Task


def add_field_subparsers(subparsers: argparse._SubParsersAction):
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "add-field", help="add a field"
    )
    parser.add_argument("name", help="the field name")
    parser.add_argument(
        "-d", "--divider", help="the divider of the score", type=int, default=1
    )
    parser.add_argument(
        "--yd", help="the year divider of the score", type=int, default=1
    )
    parser.add_argument(
        "--qd", help="the quarter divider of the score", type=int, default=1
    )
    parser.add_argument(
        "--md", help="the month divider of the score", type=int, default=1
    )
    parser.add_argument(
        "--wd", help="the week divider of the score", type=int, default=1
    )


def add_category_subparsers(subparsers: argparse._SubParsersAction):
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "add-category", help="add a category"
    )
    parser.add_argument("name", help="the category name")
    parser.add_argument(
        "-p",
        "--parent",
        help="the category parent",
        choices=[f.name for f in Category.select()],
    )
    parser.add_argument(
        "-d", "--divider", help="the divider of the score", type=int, default=1
    )
    parser.add_argument(
        "--yd", help="the year divider of the score", type=int, default=1
    )
    parser.add_argument(
        "--qd", help="the quarter divider of the score", type=int, default=1
    )
    parser.add_argument(
        "--md", help="the month divider of the score", type=int, default=1
    )
    parser.add_argument(
        "--wd", help="the week divider of the score", type=int, default=1
    )


def add_subparsers(subparsers: argparse._SubParsersAction):
    parser: argparse.ArgumentParser = subparsers.add_parser("add", help="add a task")
    parser.add_argument(
        "description", help="description of the task, aka name of the task"
    )
    parser.add_argument(
        "-s",
        "--scheduled",
        help="the date when you plan to start working on that task. Example: 2022-10-13",
    )
    parser.add_argument(
        "-e",
        "--deadline",
        help="the date when you plan to finish working on that task. Example: 2022-10-23",
    )
    parser.add_argument(
        "-r",
        "--recurrence",
        help="set the recurrence interval (the default unit is day, to change it use -u/--unit)",
        type=int,
    )
    parser.add_argument(
        "-u",
        "--unit",
        help="set the recurrence unit: d(day), w(week), m(month), y(year)",
        choices=["d", "w", "m", "y"],
    )
    parser.add_argument(
        "-f",
        "--field",
        help="set the field of task",
        choices=[f.name for f in Field.select()],
    )

    parser.add_argument(
        "-c",
        "--category",
        help="set the category of task",
        choices=[c.name for c in Category.select()],
    )

    parser.add_argument(
        "-d", "--divider", help="the divider of the score", type=int, default=1
    )
    parser.add_argument(
        "--yd", help="the year divider of the score", type=int, default=1
    )
    parser.add_argument(
        "--qd", help="the quarter divider of the score", type=int, default=1
    )
    parser.add_argument(
        "--md", help="the month divider of the score", type=int, default=1
    )
    parser.add_argument(
        "--wd", help="the week divider of the score", type=int, default=1
    )


def run_add_field_command(args: argparse.Namespace, parser: argparse.ArgumentParser):
    Field.get_or_create(
        divider=args.divider,
        week_divider=args.wd,
        month_divider=args.md,
        quarter_divider=args.qd,
        year_divider=args.yd,
        name=args.name,
    )


def run_add_category_command(args: argparse.Namespace, parser: argparse.ArgumentParser):
    parent = None
    if args.parent:
        parent = Category.get_or_none(Category.name == args.parent)
    Category.get_or_create(
        divider=args.divider,
        week_divider=args.wd,
        month_divider=args.md,
        quarter_divider=args.qd,
        year_divider=args.yd,
        name=args.name,
        category=parent,
    )


def get_day_recurrence(recurrence, unit):
    if recurrence:
        match unit:
            case "d":
                return recurrence
            case "w":
                return recurrence * 7
            case "m":
                return recurrence * 28
            case "y":
                return recurrence * 28 * 12
            case _:
                raise ValueError("How you do this?")
    return None


def run_add_command(args: argparse.Namespace, parser: argparse.ArgumentParser):
    if args.recurrence and not args.unit:
        args.unit = "d"
    elif args.unit and not args.recurrence:
        parser.error("argument -u/--unit requires -r/--recurrence")
    scheduled = None
    deadline = None
    if args.scheduled:
        if args.scheduled == "today":
            scheduled = dt.date.today()
        else:
            try:
                scheduled: dt.date = dt.datetime.strptime(
                    args.scheduled, "%Y-%m-%d"
                ).date()
            except ValueError:
                parser.error(
                    "the format of the schedule is incorrect. Try this: YYYY-MM-DD"
                )
    if args.deadline:
        if args.deadline == "today":
            deadline = dt.date.today()
        else:
            try:
                deadline: dt.date = dt.datetime.strptime(
                    args.deadline, "%Y-%m-%d"
                ).date()
            except ValueError:
                parser.error(
                    "the format of the deadline is incorrect. Try this: YYYY-MM-DD"
                )
    if deadline and scheduled and deadline < scheduled:
        parser.error("the deadline cannot be earlier than scheduled")
    field = None
    if args.field:
        field = Field.get(name=args.field)
    category = None
    if args.category:
        category = Category.get(name=args.category)
    Task.create(
        field=field,
        category=category,
        divider=args.divider,
        week_divider=args.wd,
        month_divider=args.md,
        quarter_divider=args.qd,
        year_divider=args.yd,
        description=args.description,
        scheduled=scheduled,
        deadline=deadline,
        recurrence=get_day_recurrence(args.recurrence, args.unit),
    )