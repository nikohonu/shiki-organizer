from rich.table import Table
from rich.tree import Tree

from shiki_organizer.models.database import Interval

colors = ["red", "green", "yellow", "blue", "magenta", "cyan"]
colors_map = {}
color_index = 0


def duration_to_str(duration):
    result = ""
    seconds = int(duration)
    minutes = int(duration / 60)
    hours = int(minutes / 60)
    seconds = seconds % 60
    minutes = minutes % 60
    result += f"{hours}h " if hours else ""
    result += f"{minutes}m " if minutes else ""
    result += f"{seconds}s" if seconds else ""
    return result.strip()


def _task_to_str(task):
    result = f'[bold cyan]{task["id"]}[/bold cyan]'
    excluded_tags = ["order", "parent"]
    time_tags = ["want", "duration", "average", "need"]
    if "order" in task["tags"]:
        order = next(iter(task["tags"]["order"]))
        result += f" [bold red]({order})[/bold red]"
    result += f' {task["name"]}'
    for namespace, subtags in task["tags"].items():
        if namespace not in colors_map:
            global color_index
            colors_map[namespace] = colors[color_index % 6]
            color_index += 1
        color = colors_map[namespace]
        if namespace in excluded_tags:
            continue
        for subtag in subtags:
            subtag = duration_to_str(subtag) if namespace in time_tags else subtag
            result += f" [bold {color}]{namespace}:[/bold {color}]{subtag}"
    return result


def _add_children(root_task, tasks, tree):
    leaf = tree.add(_task_to_str(root_task))
    for task in tasks:
        if (
            "parent" in task["tags"]
            and next(iter(task["tags"]["parent"])) == root_task["id"]
        ):
            _add_children(task, tasks, leaf)


def get_tree(tasks):
    tree = Tree("Tasks")
    for task in tasks:
        if "parent" not in task["tags"]:
            _add_children(task, tasks, tree)
    return tree


def get_table(tasks):
    headers_include = [
        "want",
        "need",
        "duration",
        "average",
        "scheduled",
        "days",
        "recurrence",
        "parent",
    ]
    headers = ["id", "name"]
    table = Table(title="Tasks", show_header=True, header_style="bold")
    for task in tasks:
        for key in task["tags"].keys():
            if key in headers_include and key not in headers:
                headers.append(key)
    headers.append("tags")
    for header in headers:
        if header in ["id", "recurrence", "parent"]:
            justify = "right"
        else:
            justify = "left"
        global color_index
        color = colors[color_index % 6]
        table.add_column(header, header_style=color, justify=justify)
        color_index += 1
    for task in tasks:
        row = [str(task["id"]), task["name"]]
        for header in headers[2:-1]:
            if header in task["tags"]:
                value = next(iter(task["tags"][header]))
                if header in ["duration", "average", "want", "need"]:
                    row.append(duration_to_str(value))
                else:
                    row.append(str(value))
            else:
                row.append("")
        result = ""
        for namespace, subtags in task["tags"].items():
            if namespace in headers:
                continue
            for subtag in subtags:
                result += f" {namespace}:{subtag}"
        row.append(result.strip())
        table.add_row(*row)
    return table

def get_intervals():
    return Interval.select()
