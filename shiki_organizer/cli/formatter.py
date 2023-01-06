import datetime as dt

from colorama import Fore, Style

from shiki_organizer.formatter import datetime_to_str, duration_to_str


def label_value(label, data, color):
    return f"{color}{label}:{Style.RESET_ALL}{data}"


def label_value_or_none(
    name, check, color=Fore.CYAN, data=None, unit="", space_after=True
):
    if check:
        space = " " if space_after else ""
        data = data if data else check
        if type(data) == dt.datetime:
            data = datetime_to_str(data)
        else:
            data = str(data)
        data = data if data.find(" ") == -1 else f"'{data}'"
        return f"{label_value(name, data, color)}{unit}{space}"
    else:
        return ""


def task_to_str(task, show_uuid):
    if show_uuid or not task.id:
        uuid = label_value_or_none("uuid", task.uuid, Fore.CYAN)
        id = ""
    else:
        uuid = ""
        id = f"{task.id} "
    priority = (
        f"{Fore.BLUE}({task.priority}){Style.RESET_ALL} " if task.priority else ""
    )
    scheduled = label_value_or_none("scheduled", task.scheduled, Fore.MAGENTA)
    deadline = label_value_or_none("deadline", task.deadline, Fore.RED)
    recurrence = label_value_or_none("recurrence", task.recurrence, Fore.RED, unit="d")
    days = label_value_or_none("days", task.days, Fore.BLUE)
    average = label_value_or_none(
        "average", task.average, Fore.CYAN, duration_to_str(task.average)
    )
    duration = label_value_or_none(
        "duration",
        task.duration,
        Fore.GREEN,
        duration_to_str(task.duration),
        space_after=False,
    )
    return f"{id}{priority}{task.description} {uuid}{scheduled}{recurrence}{deadline}{days}{average}{duration}"


def interval_to_str(interval, show_uuid):
    uuid = label_value_or_none("uuid", show_uuid, Fore.CYAN, interval.uuid)
    id = label_value_or_none("id", interval.id, Fore.RED)
    task = label_value_or_none(
        "task", interval.task, Fore.YELLOW, interval.task.description
    )
    start = label_value_or_none("start", interval.start, Fore.BLUE)
    end = label_value_or_none("end", interval.end, Fore.MAGENTA)
    duration = label_value_or_none(
        "duration",
        interval.duration,
        Fore.RED,
        duration_to_str(interval.duration),
        space_after=False,
    )
    return f"{uuid}{id}{task}{start}{end}{duration}"
