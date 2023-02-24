import datetime as dt
from pathlib import Path

from appdirs import user_config_dir, user_data_dir
from peewee import (
    AutoField,
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

database_path = Path(user_data_dir("shiki-organizer", "Niko Honu")) / "database.db"
database_path.parent.mkdir(parents=True, exist_ok=True)
database = SqliteDatabase(database_path, pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = database


class Namespace(BaseModel):
    id = AutoField()
    name = TextField()


class Subtag(BaseModel):
    id = AutoField()
    name = TextField()


class Tag(BaseModel):
    id = AutoField()
    namespace = ForeignKeyField(Namespace)
    subtag = ForeignKeyField(Subtag)

    @property
    def name(self):
        return f"[bold red]{self.namespace.name}:[/bold red]{self.subtag.name}"

    class Meta:
        indexes = ((("namespace", "subtag"), True),)


class Task(BaseModel):
    id = AutoField()
    name = TextField()
    parent = ForeignKeyField("self", backref="children", null=True)
    notes = TextField(null=True)


class TaskTag(BaseModel):
    id = AutoField()
    task = ForeignKeyField(Task)
    tag = ForeignKeyField(Tag)

    class Meta:
        indexes = ((("task", "tag"), True),)


class Interval(BaseModel):
    id = AutoField()
    task = ForeignKeyField(Task)
    start = DateTimeField(default=dt.datetime.now())
    end = DateTimeField(null=True)

    @property
    def duration(self):
        end = self.end if self.end else dt.datetime.now()
        return (end - self.start).seconds


models = BaseModel.__subclasses__()
database.create_tables(models)
Namespace.get_or_create(name="")
