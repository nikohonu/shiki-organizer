import datetime as dt

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

from shiki_organizer.paths import get_database_path

database_path = get_database_path()
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


models = BaseModel.__subclasses__()
database.create_tables(models)
Namespace.get_or_create(name="")
