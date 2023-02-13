import ast
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


def all():
    result = []
    for task in task_model.all():
        tags = task_model.get_tags(task)
        result.append(
            {
                "id": task.id,
                "name": task.name,
                "notes": task.notes,
                "tags": [
                    [tag.namespace.name, str_to_types(tag.subtag.name)] for tag in tags
                ],
            }
        )
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
    return [
        {
            "task_id": interval.task.id,
            "start": interval.start,
            "end": interval.end,
            "duration": interval.duration,
        }
        for interval in task_model.get_intervals()
    ]


def get_subtag(task_id, namespace):
    task = Task.get_by_id(task_id)
    namespace = Namespace.get_or_none(Namespace.name == namespace)
    if not namespace:
        return
    task_tags = (
        TaskTag.select()
        .join(Tag)
        .where((TaskTag.task == task) & (Tag.namespace == namespace))
    )
    if task_tags.count():
        tag = task_tags.get().tag
        return tag


def get_subtag_date(task_id, namespace):
    tag = get_subtag(task_id, namespace)
    if tag:
        return dt.datetime.strptime(tag.subtag.name, "%Y-%m-%d")


def get_subtag_int(task_id, namespace):
    tag = get_subtag(task_id, namespace)
    if tag:
        return int(tag.subtag.name)


def get_subtag_str(task_id, namespace):
    tag = get_subtag(task_id, namespace)
    if tag:
        return str(tag.subtag.name)


def remove_namespaces(task_id, namespaces):
    task = Task.get_by_id(task_id)
    for namespace in namespaces:
        namespace = Namespace.get_or_none(Namespace.name == namespace)
        if namespace:
            tags = Tag.select().where(Tag.namespace == namespace)
            query = TaskTag.delete().where(
                (TaskTag.task == task) & (TaskTag.tag.in_(tags))
            )
            query.execute()
