import json
from datetime import date, datetime, timedelta
from pathlib import Path

from shiki_organizer.task import Task


class Tasks:
    def __init__(self, tasks_path: Path):
        # load
        self._tasks = {}
        self._tasks_path = tasks_path
        for task_path in self._tasks_path.glob("*.json"):
            if task_path.stem.isdigit():
                identifier = int(task_path.stem)
                with task_path.open() as file:
                    data = json.load(file)
                self._tasks[identifier] = Task.from_dict(data)
        # processing
        for identifier, task in self.all().items():
            if task.scheduled and task.scheduled < date.today():
                task.scheduled = date.today()

    def __del__(self):
        for identifier, task in self.all().items():
            with (self._tasks_path / f"{identifier}.json").open("w") as file:
                json.dump(task.to_dict(), file)

    def all(self) -> dict:
        return self._tasks

    def add(
        self,
        description: str,
        scheduled: date | None,
        deadline: date | None,
        recurrence: int | None,
        unit: str | None,
    ) -> Task:
        ids = self.all().keys()
        if ids:
            identifier = max(ids) + 1
        else:
            identifier = 0
        self.all()[identifier] = Task(
            description, scheduled, deadline, recurrence, unit, False, []
        )
        return self.all()[identifier]

    def delete(self, identifier: int) -> Task:
        if identifier in self.all():
            (self._tasks_path / f"{identifier}.json").unlink()
            return self.all().pop(identifier)
        else:
            raise ValueError("the task with this id does not exist")

    def do(self, identifier: int):
        if identifier in self.all():
            task = self.all()[identifier]
            if task.recurrence != None:
                task.scheduled = (
                    datetime.today() + timedelta(days=task.interval)
                ).date()
                if task.deadline and task.scheduled > task.deadline:
                    task.is_completed = True
                    task.scheduled = None
            else:
                task.is_completed == True
            task.completions.append(datetime.now())
        else:
            raise ValueError("the task with this id does not exist")
