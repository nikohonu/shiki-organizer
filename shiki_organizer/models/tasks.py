from PySide6.QtCore import QObject, Signal

from shiki_organizer.database import Task


class Singleton(type(QObject), type):
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Tasks(QObject, metaclass=Singleton):
    updated = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.data = list(Task.select())

    #
    def __getitem__(self, key: int):
        return self.data[key].name

    def __len__(self):
        return len(self.data)

    def add(
        self,
        name,
        order=None,
        recurrence=None,
        due=None,
        until=None,
        duration_per_day=None,
        notes=None,
        parent=None,
    ):
        task = Task.create(
            name=name,
            order=order,
            notes=notes,
            recurrence=recurrence,
            due=due,
            until=until,
            duration_per_day=duration_per_day,
            parent=parent,
        )
        self.data.append(task)
        self.updated.emit()
