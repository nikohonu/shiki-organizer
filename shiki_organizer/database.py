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


class Task(BaseModel):
    name = TextField()
    order = IntegerField(null=True)
    recurrence = IntegerField(null=True)
    scheduled = DateField(null=True)
    deadline = DateField(null=True)
    parent = ForeignKeyField("self", on_delete="CASCADE", null=True)
    archived = BooleanField(default=False)
    duration = IntegerField(null=True) # using in calculation
    days = IntegerField(null=True) # using in calculation

    @property
    def average(self):
        if self.days:
            return self.duration / self.days
        else:
            return 0


class TaskTag(BaseModel):
    task = ForeignKeyField(Task)
    tag = ForeignKeyField(Tag)

    class Meta:
        primary_key = CompositeKey("task", "tag")


class Interval(BaseModel):
    task = ForeignKeyField(Task)
    start = DateTimeField(null=True)
    end = DateTimeField(null=True)

    @property
    def duration(self):
        if self.end:
            return (self.end - self.start).total_seconds()
        else:
            return (dt.datetime.now() - self.start).total_seconds()


models = BaseModel.__subclasses__()
database.create_tables(models)
