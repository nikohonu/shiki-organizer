import datetime as dt

import shiki_organizer.models.task as task_model
from shiki_organizer.database import Interval, Namespace, Subtag, Tag, Task, TaskTag


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


def task_to_dict(task, tags):
    return {
        "id": task.id,
        "name": task.name,
        "notes": task.notes,
        "tags": [[tag.namespace.name, str_to_types(tag.subtag.name)] for tag in tags],
    }


def interval_to_dict(interval):
    return {
        "task_id": interval.task.id,
        "start": interval.start,
        "end": interval.end,
        "duration": interval.duration,
    }


def all(task_ids=None):
    result = []
    for task in task_model.all(task_ids):
        tags = task_model.get_tags(task)
        result.append(task_to_dict(task, tags))
    return result


def add(name, notes, raw_tags):
    task_model.add_tags(task_model.add(name, notes), task_model.create_tags(raw_tags))


def delete(task_id):
    task_model.delete(task_model.get_by_id(task_id))


def get_ids():
    return [task.id for task in task_model.all()]


def start(task_id: int, start, end):
    task = task_model.get_by_id(task_id)
    task_model.start(task, start, end)


def stop():
    task_model.stop()


def get_intervals():
    return [interval_to_dict(interval) for interval in task_model.get_intervals()]


def get_current_interval():
    interval = task_model.get_current_interval()
    return interval_to_dict(interval) if interval else None


def tag(task_id, raw_tags):
    task_model.add_tags(task_model.get_by_id(task_id), task_model.create_tags(raw_tags))


def untag(task_id, raw_tags):
    task_model.remove_tags(
        task_model.get_by_id(task_id), task_model.create_tags(raw_tags)
    )


def get_by_id(task_id):
    return task_to_dict(task_model.get_by_id(task_id), task_model.get_tags(task_id))
