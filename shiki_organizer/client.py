import datetime as dt

from shiki_organizer.database import Interval, Namespace, Subtag, Tag, Task, TaskTag


def get_task_tags(task, ignore_namespaces=[]):
    tags = []
    namespace = Namespace.get(Namespace.name == "")
    namespaces = []
    for ignore_namespace in ignore_namespaces:
        ignore_namespace = Namespace.get_or_none(Namespace.name == ignore_namespace)
        namespaces.append(ignore_namespace)
    for task_tag in TaskTag.select().where(TaskTag.task == task):
        tag = task_tag.tag
        if tag.namespace not in namespaces:
            if tag.namespace == namespace:
                tags.append(tag.subtag.name)
            else:
                tags.append(tag.name)
    return tags


def get_tasks(ignore_namespaces=[]):
    tasks = []
    for task in Task.select():
        tags = []
        for task_tag in TaskTag.select().where(TaskTag.task == task):
            tags.append(task_tag.tag.name)
        tasks.append(
            {
                "id": task.id,
                "name": task.name,
                "tags": get_task_tags(task, ignore_namespaces),
            }
        )
    return tasks


def add_task(name, notes):
    task = Task.create(name=name, notes=notes)
    return task.id


def create_tag(name):
    if name.find(":") != -1:
        namespace, subtag = name.split(":", 1)
    else:
        namespace = ""
        subtag = name
    namespace, _ = Namespace.get_or_create(name=namespace)
    subtag, _ = Subtag.get_or_create(name=subtag)
    tag, _ = Tag.get_or_create(namespace=namespace, subtag=subtag)
    return tag


def add_tag(task, tag):
    tag = create_tag(tag)
    TaskTag.create(task=task, tag=tag)


def add_tags(task_id, tags: set):
    task = Task.get_by_id(task_id)
    for tag in tags:
        add_tag(task, tag)


def get_ids():
    return [task.id for task in Task.select()]


def delete_task(task_id):
    task = Task.get_by_id(task_id)
    task.delete_instance(recursive=True)


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
