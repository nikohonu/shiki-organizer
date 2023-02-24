import datetime as dt

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
from shiki_organizer.models.tag import (
    get_or_create_tag_from_string,
    get_or_create_tag_from_tuple,
    get_tags_from_strings,
    get_tags_from_tuples,
)


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


def get_task_ids() -> list[int]:
    return [task.id for task in Task.select()]


def tag_task(task, tags: list[Tag]) -> None:
    for tag in tags:
        TaskTag.get_or_create(task=task, tag=tag)


def tag_task_by_tuples(task, tags: list[tuple[str, str]]) -> None:
    tag_task(task, [get_or_create_tag_from_tuple(tag) for tag in tags])


def tag_task_by_strings(task, tags: list[str]) -> None:
    tag_task(task, [get_or_create_tag_from_string(tag) for tag in tags])


def add_task(
    name: str,
    notes: str | None,
    parent_id: int | None,
    order: int | None,
    scheduled: dt.date | None,
    recurrence: int | None,
    want: dt.timedelta | None,
):
    parent = Task.get_by_id(parent_id) if parent_id else None
    task = Task.create(name=name, notes=notes, parent=parent)
    task_tags: list[tuple[str, str]] = []
    task_tags.append(("order", str(order))) if order else None
    task_tags.append(("scheduled", str(scheduled))) if scheduled else None
    task_tags.append(("recurrence", str(recurrence))) if recurrence else None
    task_tags.append(("want", str(want.seconds))) if want else None
    tag_task_by_tuples(task, task_tags)
    return task


def untag_task(task, tags: list[Tag]):
    query = TaskTag.delete().where((TaskTag.task == task) & (TaskTag.tag.in_(tags)))
    query.execute()


def untag_task_by_tuples(task, tuple_tags: list[tuple[str, str]]):
    tags = get_tags_from_tuples(tuple_tags)
    untag_task(task, tags)


def untag_task_by_strings(task, string_tags: list[str]):
    tags = get_tags_from_strings(string_tags)
    untag_task(task, tags)


def modify_task(
    id: int,
    name: str | None,
    notes: str | None,
    parent_id: int | None,
    order: int | None,
    scheduled: dt.date | None,
    recurrence: int | None,
    want: dt.timedelta | None,
):
    parent = Task.get_by_id(parent_id) if parent_id else None
    task = Task.get_by_id(id)
    if name:
        task.name = name
    if notes:
        task.notes = notes
    if parent:
        task.parent = parent
    if name or notes:
        task.save()
    task_tags: list[tuple[str, str]] = []
    task_tags.append(("order", str(order))) if order else None
    task_tags.append(("scheduled", str(scheduled))) if scheduled else None
    task_tags.append(("recurrence", str(recurrence))) if recurrence else None
    task_tags.append(("want", str(want.seconds))) if want else None
    untag_task_by_tuples(task, [(namespace, "*") for namespace, _ in task_tags])
    tag_task_by_tuples(task, task_tags)
    return task


def delete_task(ids: set[int]):
    result = []
    tasks = Task.select().where(Task.id.in_(ids))
    for task in tasks:
        result.append({"id": task.id, "name": task.name})
    TaskTag.delete().where(TaskTag.task.in_(tasks)).execute()
    Interval.delete().where(Interval.task.in_(tasks)).execute()
    Task.delete().where(Task.id.in_(ids)).execute()
    return result


def _period_to_datetime(period: str) -> dt.datetime:
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
            interval = Interval.select(Interval.start).order_by(Interval.start).first()
            if interval:
                start = interval.start
            else:
                start = start.start_of("day")
            start = pendulum.datetime(year=start.year, month=start.month, day=start.day)
    start = dt.datetime(year=start.year, month=start.month, day=start.day)
    return start


def _calc_duration(tasks, period, individual_average):
    start = _period_to_datetime(period)
    intervals = Interval.select().where(Interval.start >= start)
    for interval in intervals:
        result = []
        queue = [tasks[interval.task_id]]
        while queue:
            task = queue.pop()
            result.append(task)
            if task["parent"] != None:
                queue.append(tasks[task["parent"]])
        for task in result:
            task["duration"] += interval.duration
            task["days"].add(interval.start.date())
    for id, task in tasks.items():
        if task["days"]:
            if not individual_average:
                task["days"] = (dt.datetime.now().date() - start.date()).days + 1
            else:
                task["days"] = len(task["days"])
            task["average"] = round(task["duration"] / task["days"])
        else:
            task["days"] = None
        if not individual_average and id:
            task["days"] = None
        if task["want"]:
            if task["average"]:
                task["need"] = task["want"] - task["average"]
            else:
                task["need"] = task["want"]
    return tasks


def _check_task(task, query: list[tuple[str, str, str]]):
    for key, operator, value in query:
        if key in task:
            if operator == "<=":
                if not task[key]:
                    return False
                if task[key] > value:
                    return False
    return True


def _get_tasks(include_zero=False, ids=None):
    tasks_query = Task.select()
    if ids:
        tasks_query = tasks_query.where(Task.id.in_(ids))
    tasks = {
        task.id: {
            "name": task.name,
            "parent": task.parent.id if task.parent else 0,
        }
        for task in tasks_query
    }
    if include_zero:
        tasks[0] = {"name": "Tasks", "parent": None}
    for task in tasks.values():
        task.update(
            {
                "duration": 0,
                "average": None,
                "days": set(),
                "want": None,
                "need": None,
                "scheduled": None,
                "recurrence": None,
                "status": None,
                "tags": {},
            }
        )
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
    )
    if ids:
        task_tags = task_tags.where(TaskTag.task.in_(tasks_query))
    for task_tag in task_tags.dicts():
        task = tasks[task_tag["task"]]
        if task_tag["namespace"] in task:
            task[task_tag["namespace"]] = _str_to_types(task_tag["subtag"])
        else:
            if task_tag["namespace"] in task["tags"]:
                task["tags"][task_tag["namespace"]].append(
                    _str_to_types(task_tag["subtag"])
                )
            else:
                task["tags"][task_tag["namespace"]] = [
                    _str_to_types(task_tag["subtag"])
                ]
    return tasks


def get_task(id: int):
    tasks = _get_tasks(True)
    _calc_duration(tasks, "day", True)
    return tasks[id]


def get_tasks(
    search_query: list[tuple[str, str, str]],
    period="all",
    individual_average=False,
    sorting="duration",
    completed=False,
    reverse=False,
):
    all_tasks = _get_tasks(True)
    _calc_duration(all_tasks, period, individual_average)
    if not completed:
        all_tasks = dict(
            filter(lambda item: item[1]["status"] != "completed", all_tasks.items())
        )
    filtred_tasks = {}
    if not search_query:
        filtred_tasks = all_tasks
    else:
        for id, task in all_tasks.items():
            if _check_task(task, search_query):
                filtred_tasks[id] = task
    tasks = {}
    query = list(filtred_tasks.items())
    if filtred_tasks != all_tasks:
        while query:
            current_id, current_task = query.pop()
            tasks[current_id] = current_task
            if current_task["parent"] != None:
                query.append(
                    (current_task["parent"], all_tasks[current_task["parent"]])
                )
    else:
        tasks = all_tasks
    min_key = dt.date.min if sorting in ["scheduled"] else 0
    tasks = dict(
        sorted(
            tasks.items(),
            key=lambda item: item[1][sorting] if item[1][sorting] != None else min_key,
            reverse=not reverse,
        )
    )
    return tasks


def done_tasks(ids: list[int]):
    results = []
    stop_task()
    tasks = _get_tasks(False, ids)
    for id, task in tasks.items():
        if task["status"] == "completed":
            results.append((id, task["name"], "ignored"))
            continue
        if task["recurrence"]:
            task["scheduled"] = (
                dt.datetime.now() + dt.timedelta(days=task["recurrence"])
            ).date()
            results.append((id, task["name"], "rescheduled"))
        else:
            task["status"] = "completed"
            results.append((id, task["name"], "done"))
        tags = []
        tags.append(("scheduled", task["scheduled"])) if task["scheduled"] else None
        tags.append(("status", task["status"])) if task["status"] else None
        task = Task.get_by_id(id)
        untag_task_by_tuples(task, [("scheduled", "*"), ("status", "*")])
        tag_task_by_tuples(task, tags)
    return results


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


def str_tag_to_tuple(tag: str) -> tuple[str, str]:
    if tag.find(":") != -1:
        namespace, subtag = tuple(tag.split(":", 1))
    else:
        namespace, subtag = "", tag
    return namespace, subtag
