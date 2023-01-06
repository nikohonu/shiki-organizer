import datetime as dt

from peewee import (
    BooleanField,
    CompositeKey,
    DateField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
)

from shiki_organizer.paths import get_database_path

database_path = get_database_path()
database_path.parent.mkdir(parents=True, exist_ok=True)
database = SqliteDatabase(database_path, pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = database


class Tag(BaseModel):
    name = TextField()
    notes = TextField()


class Task(BaseModel):
    created = DateTimeField(default=dt.datetime.now())
    name = TextField()
    order = IntegerField(null=True)
    notes = TextField(null=True)
    recurrence = IntegerField(null=True)
    due = DateField(null=True)
    until = DateField(null=True)
    duration_per_day = IntegerField(null=True)
    parent = ForeignKeyField("self", on_delete="CASCADE", null=True)
    archived = BooleanField(default=False)


class TaskTag(BaseModel):
    task = ForeignKeyField(Task)
    tag = ForeignKeyField(Tag)

    class Meta:
        primary_key = CompositeKey("task", "tag")


class Interval(BaseModel):
    task = ForeignKeyField(Task)
    start = DateTimeField(null=True)
    end = DateTimeField(null=True)
    duration = IntegerField(null=True)


models = BaseModel.__subclasses__()
database.create_tables(models)
