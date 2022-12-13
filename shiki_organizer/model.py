import datetime as dt
import uuid as uuid_module

from peewee import (
    BooleanField,
    DateField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
    UUIDField,
)

from shiki_organizer.utilities import get_user_data_dir

database_path = get_user_data_dir() / "data.db"
database_path.parent.mkdir(parents=True, exist_ok=True)
database = SqliteDatabase(database_path, pragmas={"foreign_keys": 1})


class BaseModel(Model):
    class Meta:
        database = database


class Task(BaseModel):
    uuid = UUIDField(primary_key=True, default=uuid_module.uuid4)
    id = IntegerField(null=True)
    created = DateTimeField(default=dt.datetime.now())
    priority = TextField(null=True)
    divider = IntegerField(default=1)
    duration = IntegerField(default=0)
    today_duration = IntegerField(default=0)
    days = IntegerField(null=True)
    description = TextField()
    recurrence = IntegerField(null=True)
    scheduled = DateField(null=True)
    deadline = DateField(null=True)
    archived = BooleanField(default=False)
    parent = ForeignKeyField("self", on_delete="CASCADE", null=True)

    @property
    def score(self):
        return self.duration / self.divider

    @property
    def today_score(self):
        return self.today_duration / self.divider

    @property
    def average(self):
        if self.days:
            return self.duration / self.days
        else:
            return 0

    @staticmethod
    def get_by_uuid(uuid):
        return Task.get(Task.uuid == uuid)

    @staticmethod
    def get_by_id(id):
        return Task.get(Task.id == id)

    @staticmethod
    def reindex():
        tasks = Task.select().order_by(Task.created)
        i = 0
        for task in tasks:
            if not task.archived:
                task.id = i + 1
                i += 1
            else:
                task.id = None
        Task.bulk_update(tasks, [Task.id])


class Interval(BaseModel):
    uuid = UUIDField(primary_key=True, default=uuid_module.uuid4)
    id = IntegerField(null=True)
    task = ForeignKeyField(Task, null=True, backref="intervals")
    start = DateTimeField(default=dt.datetime.now)
    end = DateTimeField(null=True)

    @staticmethod
    def get_by_uuid(uuid):
        return Interval.get(Interval.uuid == uuid)

    @staticmethod
    def get_by_id(id):
        return Interval.get(Interval.id == id)

    @staticmethod
    def reindex():
        intervals = Interval.select().order_by(Interval.start.desc())
        i = 0
        for interval in intervals:
            interval.id = i + 1
            i += 1
        Interval.bulk_update(intervals, [Interval.id])

    @property
    def duration(self):
        if self.end:
            return (self.end - self.start).total_seconds()
        else:
            return (dt.datetime.now() - self.start).total_seconds()


class Repository(BaseModel):
    uuid = UUIDField(primary_key=True, default=uuid_module.uuid4)
    id = IntegerField(null=True)
    created = DateTimeField(default=dt.datetime.now())
    name = TextField()
    parent = ForeignKeyField(Task, null=False, backref="repositories")

    @staticmethod
    def get_by_uuid(uuid):
        return Repository.get(Repository.uuid == uuid)

    @staticmethod
    def get_by_id(id):
        return Repository.get(Repository.id == id)

    @staticmethod
    def reindex():
        repositories = Repository.select().order_by(Repository.created.desc())
        i = 0
        for repository in repositories:
            repository.id = i + 1
            i += 1
        Repository.bulk_update(repositories, [Task.id])


class Issue(BaseModel):
    uuid = UUIDField(primary_key=True, default=uuid_module.uuid4)
    repository = ForeignKeyField(Repository, backref="issues")
    id = IntegerField(null=False)
    name = TextField(null=True)
    task = ForeignKeyField(Task, backref="issue", null=True)


models = BaseModel.__subclasses__()
database.create_tables(models)
