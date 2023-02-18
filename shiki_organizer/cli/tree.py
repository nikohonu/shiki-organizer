from rich.tree import Tree

from shiki_organizer.cli.style import colors, duration_to_str


def task_to_str(task):
    def tags_to_str(tags):
        result = ""
        for namespace in tags:
            for subtag in tags[namespace]:
                result += f" [yellow]{namespace}:[/yellow]{subtag}"
        return result

    result = f"{task['id']} {task['name']}"
    for key, value in task.items():
        if key not in ["id", "name", "notes", "parent"]:
            if key == "tags" and task["tags"]:
                result += tags_to_str(task["tags"])
            elif key != "tags":
                if key in ["duration", "average"]:
                    value = duration_to_str(value, style="gray")
                if key in colors:
                    result += f" [{colors[key]}]{key}:[/{colors[key]}]{value}"
                else:
                    result += f" {key}:{value}"
    return result


def add_children(task, tasks, tree):
    leaf = tree.add(task_to_str(task))
    for child in tasks:
        if "parent" in child and child["parent"] == task["id"]:
            add_children(child, tasks, leaf)


def create_tasks_tree(tasks):
    tree = Tree("Tasks")
    for task in tasks:
        if "parent" not in task:
            add_children(task, tasks, tree)
    return tree
