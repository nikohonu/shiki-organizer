import argparse

from shiki_organizer.model import Category, Field, Task


def del_category_subparsers(subparsers: argparse._SubParsersAction):
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "del-category", help="delete the category"
    )
    parser.add_argument(
        "name",
        help="the category name",
        choices=[c.name for c in Category.select()],
    )


def del_subparsers(subparsers: argparse._SubParsersAction):
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "del", help="delete the task"
    )
    parser.add_argument(
        "id", help="the task id", type=int, choices=[t.id for t in Task.select()]
    )


def del_field_subparsers(subparsers: argparse._SubParsersAction):
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "del-field", help="delete the field"
    )
    parser.add_argument(
        "name",
        help="the field name",
        choices=[f.name for f in Field.select()],
    )


def run_del_category_command(args: argparse.Namespace, parser: argparse.ArgumentParser):
    Category.get(Category.name == args.name).delete_instance(recursive=True)


def run_del_command(args: argparse.Namespace, parser: argparse.ArgumentParser):
    Task.get_by_id(args.id).delete_instance(recursive=True)


def run_del_field_command(args: argparse.Namespace, parser: argparse.ArgumentParser):
    Field.get(Field.name == args.name).delete_instance(recursive=True)