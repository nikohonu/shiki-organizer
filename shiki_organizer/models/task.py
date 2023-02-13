import datetime as dt

from shiki_organizer.database import Interval, Namespace, Subtag, Tag, Task, TaskTag


def get_tags(task):
    return [task_tag.tag for task_tag in TaskTag.select().where(TaskTag.task == task)]


def all():
    return [task for task in Task.select()]


def add(name, notes):
    task = Task.create(name=name, notes=notes)
    return task


def create_tags(raw_tags):
    tags = []
    namespaces = {}
    subtags = {}
    for namespace, subtag in raw_tags:
        if namespace not in namespaces:
            namespaces[namespace], _ = Namespace.get_or_create(name=namespace)
        if subtag not in subtags:
            subtags[subtag], _ = Subtag.get_or_create(name=subtag)
        tag, _ = Tag.get_or_create(
            namespace=namespaces[namespace], subtag=subtags[subtag]
        )
        tags.append(tag)
    return tags


def add_tags(task, tags):
    for tag in tags:
        TaskTag.get_or_create(task=task, tag=tag)


def get_by_id(task_id):
    return Task.get_by_id(task_id)


def delete(task):
    task.delete_instance(recursive=True)


def start(task, start, end):
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


def stop():
    interval = Interval.get_or_none(Interval.end == None)
    if interval:
        interval.end = dt.datetime.now()
        interval.save()


def get_intervals():
    return Interval.select()
