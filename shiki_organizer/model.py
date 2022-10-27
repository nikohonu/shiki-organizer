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

database_path = get_user_data_dir() / "database.db"
database_path.parent.mkdir(parents=True, exist_ok=True)
database = SqliteDatabase(
    database_path, pragmas={"foreign_keys": 1}
)


class BaseModel(Model):
    class Meta:
        database = database


class Category(BaseModel):
    divider = IntegerField(default=1)
    week_divider = IntegerField(default=1)
    month_divider = IntegerField(default=1)
    quarter_divider = IntegerField(default=1)
    year_divider = IntegerField(default=1)
    name = TextField(unique=True)
    category = ForeignKeyField('self', on_delete="CASCADE", null=True)


class Field(BaseModel):
    divider = IntegerField(default=1)
    week_divider = IntegerField(default=1)
    month_divider = IntegerField(default=1)
    quarter_divider = IntegerField(default=1)
    year_divider = IntegerField(default=1)
    name = TextField(unique=True)


class Task(BaseModel):
    field = ForeignKeyField(Field, on_delete="CASCADE", null=True)
    category = ForeignKeyField(Category, on_delete="CASCADE", null=True)

    divider = IntegerField(default=1)
    week_divider = IntegerField(default=1)
    month_divider = IntegerField(default=1)
    quarter_divider = IntegerField(default=1)
    year_divider = IntegerField(default=1)
    description = TextField()
    scheduled = DateField(null=True)
    deadline = DateField(null=True)
    recurrence = IntegerField(null=True)
    is_completed = BooleanField(default=False)
    is_hidden = BooleanField(default=False)

    @property
    def days(self):
        dates = set()
        for interval in Interval.select(Interval.start).where(Interval.task == self):
            dates.add(interval.start.date())
        return len(dates)

    @property
    def duration(self):
        durations = list()
        for interval in Interval.select().where(Interval.task == self):
            durations.append(interval.duration)
        return sum(durations)



class Skill(BaseModel):
    name = TextField()


class TaskSkill(BaseModel):
    task = ForeignKeyField(Task, on_delete="CASCADE")
    skill = ForeignKeyField(Skill, on_delete="CASCADE")

    class Meta:
        primary_key = CompositeKey("task", "skill")


class Interval(BaseModel):
    task = ForeignKeyField(Task, on_delete="CASCADE")

    start = DateTimeField(default=dt.datetime.now)
    end = DateTimeField(null=True)

    @property
    def duration(self):
        if self.end:
            return (self.end - self.start).total_seconds()
        else:
            return (dt.datetime.now() - self.start).total_seconds()



models = BaseModel.__subclasses__()
database.create_tables(models)
