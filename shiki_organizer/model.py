import datetime as dt
import uuid as uuid_module

from peewee import (
    BooleanField,
    DateField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    ManyToManyField,
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


class Project(BaseModel):
    name = TextField()

    @staticmethod
    def remove_unused():
        tasks = Task.select()
        for project in Project.select():
            if tasks.where(Task.project == project).count() == 0:
                project.delete_instance()


class Tag(BaseModel):
    name = TextField()

    @staticmethod
    def remove_unused():
        tasks = TaskTag.select()
        for tag in Tag.select():
            if tasks.where(TaskTag.tag == tag).count() == 0:
                tag.delete_instance()


class Task(BaseModel):
    uuid = UUIDField(primary_key=True, default=uuid_module.uuid4)
    id = IntegerField(null=True)
    created = DateTimeField(default=dt.datetime.now())
    priority = TextField(null=True)
    description = TextField()
    recurrence = IntegerField(null=True)
    scheduled = DateField(null=True)
    deadline = DateField(null=True)
    archived = BooleanField(default=False)
    project = ForeignKeyField(Project, null=True, backref="tasks")
    tags = ManyToManyField(Tag, backref="tasks")

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


TaskTag = Task.tags.get_through_model()


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


models = BaseModel.__subclasses__() + [TaskTag]
database.create_tables(models)
