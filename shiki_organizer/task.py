import datetime as dt

from peewee import JOIN

import shiki_organizer.models.task as task_model
from shiki_organizer.database import Interval, Namespace, Subtag, Tag, Task, TaskTag
from shiki_organizer.model import build_dict, cur


def str_to_types(string: str):
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


def _task_to_dict(task, tags):
    return {
        "id": task.id,
        "name": task.name,
        "notes": task.notes,
        "tags": [[tag.namespace.name, str_to_types(tag.subtag.name)] for tag in tags],
    }


def _interval_to_dict(interval):
    return {
        "id": interval.id,
        "task_id": interval.task.id,
        "start": interval.start,
        "end": interval.end,
        "duration": interval.duration,
    }


def all(task_ids=None):
    tasks = build_dict(
        cur.execute("SELECT id, name, notes FROM task").fetchall(),
        ["id", "name", "notes"],
    )
    tasks_tags = build_dict(
        cur.execute(
            "SELECT tasktag.task_id, namespace.name, subtag.name from tasktag "
            "JOIN tag on tasktag.tag_id = tag.id "
            "JOIN namespace ON tag.namespace_id = namespace.id "
            "JOIN subtag ON tag.subtag_id = subtag.id"
        ).fetchall(),
        ["task_id", "namespace", "subtag"],
    )
    for task in tasks:
        raw_tags = [
            (task_tag["namespace"], str_to_types(task_tag["subtag"]))
            for task_tag in tasks_tags
            if task_tag["task_id"] == task["id"]
        ]
        tags = {}
        for namespace, subtag in raw_tags:
            if namespace in tags:
                tags[namespace].append(subtag)
            else:
                tags[namespace] = [subtag]
        task["tags"] = tags
    if task_ids:
        return [task for task in tasks if task["id"] in task_ids]
    else:
        return tasks


def add(name, notes, raw_tags):
    task = task_model.add(name, notes)
    task_model.add_tags(task, task_model.create_tags(raw_tags))
    return task.id


def delete(task_id):
    task = task_model.get_by_id(task_id)
    id, name = task.id, task.name
    task_model.delete(task)
    return id, name


def get_ids():
    return [task.id for task in task_model.all()]


def start(task_id: int, start, end):
    task = task_model.get_by_id(task_id)
    task_model.start(task, start, end)


def stop():
    task_model.stop()


def get_intervals():
    return [_interval_to_dict(interval) for interval in task_model.get_intervals()]


def get_current_interval():
    interval = task_model.get_current_interval()
    return _interval_to_dict(interval) if interval else None


def tag(task_id, raw_tags):
    task_model.add_tags(task_model.get_by_id(task_id), task_model.create_tags(raw_tags))


def untag(task_id, raw_tags):
    task_model.remove_tags(
        task_model.get_by_id(task_id), task_model.create_tags(raw_tags)
    )


def get_by_id(task_id):
    return _task_to_dict(task_model.get_by_id(task_id), task_model.get_tags(task_id))
