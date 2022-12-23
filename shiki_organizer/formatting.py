from colorama import Fore, Style
import datetime as dt


def _duration_to_str(duration):
    seconds = int(duration)
    minutes = int(duration / 60)
    hours = int(minutes / 60)
    seconds = seconds % 60
    minutes = minutes % 60
    hours = f"{hours}h " if hours else "" 
    return f"{hours}{minutes}m {seconds}s"

def _get(name, check, color=Fore.CYAN, data=None, unit="", space_after=True):
    if check:
        space = " " if space_after else ""
        data = data if data else check
        if type(data) == dt.datetime:
            data = data.isoformat(" ", "seconds")
        else:
            data = str(data)
        data = data if data.find(" ") == -1 else f"'{data}'" 
        return f"{color}{name}:{Style.RESET_ALL}{data}{unit}{space}"
    else:
        return ""


def task_to_str(task, show_uuid):
    if show_uuid or not task.id:
        uuid = _get("uuid", task.uuid, Fore.CYAN)
        id = ""
    else:
        uuid = ""
        id = f"{task.id} "
    priority = (
        f"{Fore.BLUE}({task.priority}){Style.RESET_ALL} " if task.priority else ""
    )
    scheduled = _get("scheduled", task.scheduled, Fore.MAGENTA)
    deadline = _get("deadline", task.deadline, Fore.RED)
    recurrence = _get("recurrence", task.recurrence, Fore.RED, unit="d")
    days = _get("days", task.days, Fore.BLUE)
    average = _get("average", task.average, Fore.CYAN, _duration_to_str(task.average))
    duration = _get(
        "duration",
        task.duration,
        Fore.GREEN,
        _duration_to_str(task.duration),
        space_after=False,
    )
    return f"{id}{priority}{task.description} {uuid}{scheduled}{recurrence}{deadline}{days}{average}{duration}"


def interval_to_str(interval, show_uuid):
    uuid = _get("uuid", show_uuid, Fore.CYAN, interval.uuid)
    id = _get("id", interval.id, Fore.RED)
    task = _get("task", interval.task, Fore.YELLOW, interval.task.description)
    start = _get("start", interval.start, Fore.BLUE)
    end = _get("end", interval.end, Fore.MAGENTA)
    duration = _get(
        "duration",
        interval.duration,
        Fore.RED,
        _duration_to_str(interval.duration),
        space_after=False,
    )
    return f"{uuid}{id}{task}{start}{end}{duration}"
