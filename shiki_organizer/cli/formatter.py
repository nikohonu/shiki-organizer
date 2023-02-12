import datetime as dt

from shiki_organizer.formatter import datetime_to_str, duration_to_str


def label_value(label, data, color):
    return f"[{color}]{label}:[/{color}]{data}"


def label_value_or_none(
    name, check, color="cyan", data=None, unit="", space_after=True
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


def task_to_str(task, show_id=True):
    if show_id:
        id = f"{task.id} "
    else:
        id = ""
    order = f"[blue]({task.order}) [/blue]" if task.order else ""
    scheduled = label_value_or_none("scheduled", task.scheduled, "magenta")
    recurrence = label_value_or_none("recurrence", task.recurrence, "red", unit="d")
    deadline = label_value_or_none("deadline", task.deadline, "red")
    days = label_value_or_none("days", task.days, "blue")
    average = label_value_or_none(
        "average", task.average, "cyan", duration_to_str(task.average)
    )
    duration = label_value_or_none(
        "duration",
        task.duration,
        "green",
        duration_to_str(task.duration),
        space_after=False,
    )
    return f"{id}{order}{task.name} {scheduled}{recurrence}{deadline}{days}{average}{duration}".strip()


def interval_to_str(interval, show_uuid):
    uuid = label_value_or_none("uuid", show_uuid, Fore.CYAN, interval.uuid)
    id = label_value_or_none("id", interval.id, Fore.RED)
    task = label_value_or_none("task", interval.task, Fore.YELLOW, interval.task.name)
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
