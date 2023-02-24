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


def _str_tag_to_tuple(tag: str) -> tuple[str, str]:
    if tag.find(":") != -1:
        namespace, subtag = tuple(tag.split(":", 1))
    else:
        namespace, subtag = "", tag
    return namespace, subtag


def get_or_create_tag_from_tuple(new_tag: tuple[str, str]) -> Tag:
    namespace, subtag = new_tag
    if subtag == "*":
        RuntimeError('the tag subtag cannot be "*"')
    namespace, _ = Namespace.get_or_create(name=namespace)
    subtag, _ = Subtag.get_or_create(name=subtag)
    tag, _ = Tag.get_or_create(namespace=namespace, subtag=subtag)
    return tag


def get_or_create_tag_from_string(new_tag: str) -> Tag:
    return get_or_create_tag_from_tuple(_str_tag_to_tuple(new_tag))


def get_tags_from_tuples(tags: list[tuple[str, str]]) -> list[Tag]:
    local_tags = set()
    for namespace, subtag in tags:
        if subtag == "*":
            namespace, _ = Namespace.get_or_create(name=namespace)
            local_tags |= set(Tag.select().where(Tag.namespace == namespace))
        else:
            local_tags.add(get_or_create_tag_from_tuple((namespace, subtag)))
    return list(local_tags)


def get_tags_from_strings(tags: list[str]) -> list[Tag]:
    tags_as_tuples = [_str_tag_to_tuple(tag) for tag in tags]
    return get_tags_from_tuples(tags_as_tuples)
