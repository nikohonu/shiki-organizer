from datetime import date, datetime, timedelta


def gt(dt_str):
    dt, _, us = dt_str.partition(".")
    dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    us = int(us.rstrip("Z"), 10)
    return dt + timedelta(microseconds=us)


class Task:
    def __init__(
        self,
        description: str,
        scheduled: date | None,
        deadline: date | None,
        recurrence: int | None,
        unit: str | None,
        is_completed: bool,
        completions: list 
    ) -> None:
        self.description: str = description
        self.scheduled: date = scheduled
        self.deadline: date = deadline
        self.recurrence: date = recurrence
        self.unit: date = unit
        self.is_completed = is_completed
        self.completions = completions

    @property
    def interval(self):
        match self.unit:
            case "d":
                return self.recurrence
            case "w":
                return self.recurrence * 7
            case "m":
                return self.recurrence * 28
            case "y":
                return self.recurrence * 28 * 12
            case _:
                raise ValueError("How you do this?")

    @classmethod
    def from_dict(cls, data: dict):
        scheduled = (
            datetime.strptime(data["scheduled"], "%Y-%m-%d").date()
            if data["scheduled"]
            else None
        )
        deadline = (
            datetime.strptime(data["deadline"], "%Y-%m-%d").date()
            if data["deadline"]
            else None
        )
        is_completed = data["is_completed"] if "is_completed" in data else False
        completions = [gt(completion) for completion in data["completions"]] if "completions" in data else []
        return Task(
            # identifier,
            data["description"],
            scheduled,
            deadline,
            data["recurrence"],
            data["unit"],
            is_completed,
            completions,
        )

    def to_dict(self):
        return {
            "description": self.description,
            "scheduled": self.scheduled.isoformat() if self.scheduled else None,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "recurrence": self.recurrence,
            "unit": self.unit,
            "is_completed": self.is_completed,
            "completions": [completion.isoformat() for completion in self.completions]
        }

