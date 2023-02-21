import datetime as dt
from typing import List, Set, Tuple

import pendulum

from shiki_organizer.formatting import console
from shiki_organizer.models.database import (
    Interval,
    Namespace,
    Subtag,
    Tag,
    Task,
    TaskTag,
)


def str_tag_to_tuple(tag):
    if tag.find(":") != -1:
        tag = tuple(tag.split(":", 1))
    else:
        tag = ("", tag)
    return tag


def _str_to_types(string: str):
    try:
        datetime = dt.datetime.strptime(string, "%Y-%m-%d")
        return datetime.date()
    except ValueError:
        pass
    try:
        datetime = dt.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S")
        return datetime
    except ValueError:
        pass
    try:
        return float(string) if "." in string else int(string)
    except ValueError:
        return string


def get_task_ids():
    return [task.id for task in Task.select()]


def add_task(
    name: str,
    notes: str | None,
    parent_id: int | None,
    order: int | None,
    scheduled: dt.date | None,
    recurrence: int | None,
    want: int | None,
    tags: List[str],
):
    task = Task.create(name=name, notes=notes)
    task_tags = {str_tag_to_tuple(tag) for tag in tags}
    task_tags.add(("parent", str(parent_id))) if parent_id else None
    task_tags.add(("order", str(order))) if order else None
    task_tags.add(("scheduled", str(scheduled))) if scheduled else None
    task_tags.add(("recurrence", str(recurrence))) if recurrence else None
    task_tags.add(("want", str(want))) if recurrence else None
    tag_task(task, task_tags)
    return task


def tag_task(task, tags: Set[tuple]):
    for namespace, subtag in tags:
        namespace, _ = Namespace.get_or_create(name=namespace)
        subtag, _ = Subtag.get_or_create(name=subtag)
        tag, _ = Tag.get_or_create(namespace=namespace, subtag=subtag)
        TaskTag.create(task=task, tag=tag)


def untag_task(task, tags: Set[tuple]):
    for namespace, subtag in tags:
        namespace, _ = Namespace.get_or_create(name=namespace)
        if subtag == "*":
            target_tags = Tag.select().where(Tag.namespace == namespace)
        else:
            subtag, _ = Subtag.get_or_create(name=subtag)
            target_tags = Tag.select().where(
                Tag.namespace == namespace, Tag.subtag == subtag
            )
        query = TaskTag.delete().where(
            (TaskTag.task == task) & (TaskTag.tag.in_(target_tags))
        )
        query.execute()


def modify_task(
    id: int,
    name: str | None,
    notes: str | None,
    parent_id: int | None,
    order: int | None,
    scheduled: dt.date | None,
    recurrence: int | None,
    want: int | None,
):
    task = Task.get_by_id(id)
    if name:
        task.name = name
    if notes:
        task.notes = notes
    if name or notes:
        task.save()
    task_tags = set()
    task_tags.add(("parent", str(parent_id))) if parent_id else None
    task_tags.add(("order", str(order))) if order else None
    task_tags.add(("scheduled", str(scheduled))) if scheduled else None
    task_tags.add(("recurrence", str(recurrence))) if recurrence else None
    task_tags.add(("want", str(want))) if want else None
    untag_task(task, {(namespace, "*") for namespace, _ in task_tags})
    tag_task(task, task_tags)
    return task


def delete_task(ids: List[int]):
    result = []
    tasks = Task.select().where(Task.id.in_(ids))
    for task in tasks:
        result.append({"id": task.id, "name": task.name})
    TaskTag.delete().where(TaskTag.task.in_(tasks)).execute()
    Interval.delete().where(Interval.task.in_(tasks)).execute()
    Task.delete().where(Task.id.in_(ids)).execute()
    return result


def _period_to_datetime(period: str, min_start):
    start = pendulum.now()
    match period.lower():
        case "day":
            start = start.start_of("day")
        case "week":
            start = start.start_of("week")
        case "month":
            start = start.start_of("month")
        case "year":
            start = start.start_of("year")
        case _:
            start = min_start
    if start != min_start:
        start_string = start.to_datetime_string()
        start = dt.datetime.fromisoformat(start_string)
    return start


def _calc_duration(tasks, period, individual_average):
    local_tasks = {
        task["id"]: {
            "parent": next(iter(task["tags"]["parent"]))
            if "parent" in task["tags"]
            else None,
            "duration": 0,
            "days": set(),
        }
        for task in tasks
    }
    start = dt.datetime.max
    intervals = Interval.select()
    for interval in intervals:
        if interval.start < start:
            start = interval.start
    start = _period_to_datetime(period, start)
    intervals = intervals.where(Interval.start >= start)
    for interval in intervals:
        result = []
        queue = [local_tasks[interval.task_id]]
        while queue:
            task = queue.pop()
            result.append(task)
            if task["parent"]:
                queue.append(local_tasks[task["parent"]])
        for task in result:
            task["duration"] += interval.duration
            task["days"].add(interval.start.date())
    for task in local_tasks.values():
        if task["days"]:
            if not individual_average:
                task["days"] = (dt.datetime.now() - start).days + 1
            else:
                task["days"] = len(task["days"])
            task["average"] = round(task["duration"] / task["days"])
    for task in tasks:
        duration = local_tasks[task["id"]]["duration"]
        if duration:
            days = local_tasks[task["id"]]["days"]
            average = local_tasks[task["id"]]["average"]
            task["tags"]["duration"] = [duration]
            task["tags"]["average"] = [average]
            if individual_average:
                task["tags"]["days"] = [days]
            if "want" in task["tags"]:
                need = next(iter(task["tags"]["want"])) - average
                task["tags"]["need"] = [need]


def get_tasks(
    duration=False,
    period="all",
    individual_average=False,
    completed=False,
    sorting="duration",
    reverse=False,
):
    tasks = Task.select().dicts()
    task_tags = (
        TaskTag.select(
            TaskTag.task,
            Namespace.name.alias("namespace"),
            Subtag.name.alias("subtag"),
            Tag.subtag,
        )
        .join(Tag)
        .join_from(Tag, Namespace)
        .join_from(Tag, Subtag)
    ).dicts()
    for task in tasks:
        local_task_tags = [
            task_tag for task_tag in task_tags if task_tag["task"] == task["id"]
        ]
        task["tags"] = {}
        for tag in local_task_tags:
            if tag["namespace"] not in task["tags"]:
                task["tags"][tag["namespace"]] = [_str_to_types(tag["subtag"])]
            else:
                task["tags"][tag["namespace"]].append(_str_to_types(tag["subtag"]))
        task["tags"] = dict(sorted(task["tags"].items()))
    if duration:
        _calc_duration(tasks, period, individual_average)
        if not completed:
            tasks = list(
                filter(
                    lambda t: next(iter(t["tags"]["status"])) != "completed"
                    if "status" in t["tags"]
                    else True,
                    tasks,
                )
            )
        min_key = dt.date.min if sorting in ["scheduled"] else 0
        tasks = sorted(
            tasks,
            key=lambda t: next(iter(t["tags"][sorting]))
            if sorting in t["tags"]
            else min_key,
            reverse=reverse,
        )
    return tasks


def get_current_interval():
    return Interval.get_or_none(Interval.end == None)


def start_task(task_id: int, start, end):
    task = Task.get_by_id(task_id)
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        if interval.task == task:
            return
        else:
            interval.end = dt.datetime.now()
            interval.save()
    if end and end < start:
        end = None
        return
    Interval.create(task=task, start=start, end=end)


def stop_task():
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        interval.end = dt.datetime.now()
        interval.save()


def get_task_by_id(id):
    return Task.get_by_id(id)
