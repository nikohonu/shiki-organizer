import datetime as dt
from typing import List, Set, Tuple

from shiki_organizer.models.database import (
    Interval,
    Namespace,
    Subtag,
    Tag,
    Task,
    TaskTag,
)


def _str_tag_to_tuple(tag):
    if tag.find(":") != -1:
        tag = tuple(tag.split(":", 1))
    else:
        tag = ("", tag)
    return tag


def get_task_ids():
    return [task.id for task in Task.select()]


def add_task(
    name: str,
    notes: str | None,
    parent_id: int | None,
    order: int | None,
    scheduled: dt.date | None,
    recurrence: int | None,
    tags: List[str],
):
    task = Task.create(name=name, notes=notes)
    task_tags = {_str_tag_to_tuple(tag) for tag in tags}
    task_tags.add(("parent", str(parent_id))) if parent_id else None
    task_tags.add(("order", str(order))) if order else None
    task_tags.add(("scheduled", str(scheduled))) if scheduled else None
    task_tags.add(("recurrence", str(recurrence))) if recurrence else None
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
    untag_task(task, {(namespace, "*") for namespace, _ in task_tags})
    tag_task(task, task_tags)
    return task
