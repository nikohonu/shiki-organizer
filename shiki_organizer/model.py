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

from shiki_organizer.utilities import get_user_data_dir

database_path = get_user_data_dir() / "data.db"
database_path.parent.mkdir(parents=True, exist_ok=True)
database = SqliteDatabase(database_path, pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = database


class Task(BaseModel):
    rating = IntegerField(default=1000)
    divider = IntegerField(default=1)
    name = TextField()
    recurrence = IntegerField(null=True)
    scheduled = DateField(null=True)
    deadline = DateField(null=True)
    archived = BooleanField(default=False)

    # @property
    # def days(self):
    #     dates = set()
    #     for interval in Interval.select(Interval.start).where(Interval.task == self):
    #         dates.add(interval.start.date())
    #     return len(dates)

    # @property
    # def duration(self):
    #     durations = list()
    #     for interval in Interval.select().where(Interval.task == self):
    #         durations.append(interval.duration)
    #     return sum(durations)


class TaskTask(BaseModel):
    child = ForeignKeyField(Task, on_delete="CASCADE")
    parent = ForeignKeyField(Task, on_delete="CASCADE")

    class Meta:
        primary_key = CompositeKey("child", "parent")


class Interval(BaseModel):
    start = DateTimeField(default=dt.datetime.now)
    end = DateTimeField(null=True)

    @property
    def duration(self):
        if self.end:
            return (self.end - self.start).total_seconds()
        else:
            return (dt.datetime.now() - self.start).total_seconds()


class IntervalTask(BaseModel):
    interval = ForeignKeyField(Interval, on_delete="CASCADE")
    task = ForeignKeyField(Task, on_delete="CASCADE")

    class Meta:
        primary_key = CompositeKey("interval", "task")


models = BaseModel.__subclasses__()
database.create_tables(models)