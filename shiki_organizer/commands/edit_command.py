import argparse
import datetime as dt

from shiki_organizer.model import Category, Field, Task


def edit_field_subparsers(subparsers: argparse._SubParsersAction):
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "edit-field", help="edit the field"
    )
    parser.add_argument(
        "name", help="the field name", choices=[f.name for f in Field.select()]
    )
    parser.add_argument("-n", "--new-name", help="the new field name")
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


def edit_category_subparsers(subparsers: argparse._SubParsersAction):
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "edit-category", help="edit the category"
    )
    parser.add_argument(
        "name", help="the category name", choices=[c.name for c in Category.select()]
    )
    parser.add_argument("-n", "--new-name", help="the new category name")
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


def edit_subparsers(subparsers: argparse._SubParsersAction):
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "edit", help="edit the task"
    )
    parser.add_argument(
        "id", help="id of the task", type=int, choices=[t.id for t in Task.select()]
    )

    parser.add_argument(
        "-n", "--description", help="description of the task, aka name of the task"
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
        "--rr",
        help="reset recurence",
        action='store_true',
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


def run_edit_field_command(args: argparse.Namespace, parser: argparse.ArgumentParser):
    field = Field.get(Field.name == args.name)
    field.divider = args.divider if args.divider else field.divider
    field.week_divider = args.wd if args.wd else field.week_divider
    field.month_divider = args.md if args.md else field.month_divider
    field.quarter_divider = args.qd if args.qd else field.quarter_divider
    field.year_divider = args.yd if args.yd else field.year_divider
    field.name = args.new_name if args.new_name else field.name
    field.save()


def run_edit_category_command(
    args: argparse.Namespace, parser: argparse.ArgumentParser
):
    parent = None
    if args.parent:
        parent = Category.get_or_none(Category.name == args.parent)
    category = Category.get(Category.name == args.name)
    category.divider = args.divider if args.divider else category.divider
    category.week_divider = args.wd if args.wd else category.week_divider
    category.month_divider = args.md if args.md else category.month_divider
    category.quarter_divider = args.qd if args.qd else category.quarter_divider
    category.year_divider = args.yd if args.yd else category.year_divider
    category.name = args.new_name if args.new_name else category.name
    category.category = parent if parent else category.category
    category.save()


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


def run_edit_command(args: argparse.Namespace, parser: argparse.ArgumentParser):
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

    task = Task.get_by_id(args.id)
    task.field = field if field else task.field
    task.category = category if category else task.category
    task.divider = args.divider if args.divider else task.divider
    task.week_divider = args.wd if args.wd else task.week_divider
    task.month_divider = args.md if args.md else task.month_divider
    task.quarter_divider = args.qd if args.qd else task.quarter_divider
    task.year_divider = args.yd if args.yd else task.year_divider
    task.description = args.description if args.description else task.description
    task.scheduled = scheduled if scheduled else task.scheduled
    if args.rr: 
        task.recurrence = None
    else:
        task.recurrence = (
            get_day_recurrence(args.recurrence, args.unit)
            if get_day_recurrence(args.recurrence, args.unit)
            else task.recurrence
        )
    task.save()
