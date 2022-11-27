import datetime as dt

from peewee import (
    BooleanField,
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
    name = TextField()
    recurrence = IntegerField(null=True)
    scheduled = DateField(null=True)
    deadline = DateField(null=True)
    archived = BooleanField(default=False)
    parent = ForeignKeyField("self", on_delete="CASCADE", null=True)

    @property
    def parents(self):
        result = []
        q = self.parent
        while q:
            result.append(q)
            q = q.parent
        return result

    @property
    def children(self):
        result = []
        queue = list(Task.select().where(Task.parent == self))
        while queue:
            task = queue.pop()
            queue += list(Task.select().where(Task.parent == task))
            result.append(task)
        return result

    @property
    def direct_children(self):
        return list(Task.select().where(Task.parent == self))


class Interval(BaseModel):
    start = DateTimeField(default=dt.datetime.now)
    end = DateTimeField(null=True)
    task = ForeignKeyField(Task, on_delete="CASCADE")

    @property
    def duration(self):
        if self.end:
            return (self.end - self.start).total_seconds()
        else:
            return (dt.datetime.now() - self.start).total_seconds()


models = BaseModel.__subclasses__()
database.create_tables(models)