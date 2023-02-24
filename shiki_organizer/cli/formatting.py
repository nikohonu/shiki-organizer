from rich.tree import Tree

colors = ["red", "green", "yellow", "blue", "magenta", "cyan"]
colors_map = {}
color_index = 0


def duration_to_str(duration):
    if duration <= 0:
        result = "-"
        duration = -duration
    else:
        result = ""
    seconds = duration
    minutes = int(duration / 60)
    hours = int(minutes / 60)
    seconds = seconds % 60
    minutes = minutes % 60
    result += f"{hours}h " if hours else ""
    result += f"{minutes}m " if minutes else ""
    result += f"{seconds}s" if seconds else ""
    return result.strip()


def _task_to_str(id, task):
    result = f"[bold cyan]{id}[/bold cyan]"
    excluded_tags = ["order", "parent", "name"]
    time_tags = ["want", "duration", "average", "need"]
    if "order" in task["tags"]:
        order = next(iter(task["tags"]["order"]))
        result += f" [bold red]({order})[/bold red]"
    result += f' {task["name"]}'
    for key, value in task.items():
        if not value:
            continue
        if key in excluded_tags:
            continue
        if key in time_tags:
            value = duration_to_str(value)
        if key not in colors_map:
            global color_index
            colors_map[key] = colors[color_index % 6]
            color_index += 1
        color = colors_map[key]
        result += f" [bold {color}]{key}:[/bold {color}]{value}"
    return result


def get_tree(root_id, tasks, node=None):
    if node == None:
        node = Tree(_task_to_str(root_id, tasks[root_id]))
    else:
        node = node.add(_task_to_str(root_id, tasks[root_id]))
    for key, task in tasks.items():
        if task["parent"] == root_id:
            get_tree(key, tasks, node)
    return node
