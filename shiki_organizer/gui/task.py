import datetime as dt
import os

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QBrush, QColor

import shiki_organizer.actions as actions
from shiki_organizer.formatter import duration_to_str
from shiki_organizer.model import Task


class TaskModel(QAbstractTableModel):
    def __init__(self, today=True, parent=None):
        super().__init__(parent)
        self.today = today
        tasks = Task.select().where(Task.archived == False)
        if self.today:
            tasks = tasks.where(Task.scheduled <= dt.date.today())
        self._tasks = [task for task in tasks]
        self._headers = [
            "ID",
            "Priority",
            "Description",
            "Recurrence",
            "Scheduled",
            "Deadline",
            "Days",
            "Average",
            "Duration",
        ]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if orientation == Qt.Orientation.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return super().headerData(section, orientation, role)

    def data(self, index: QModelIndex, role: int):
        if index.isValid():
            if role == Qt.DisplayRole:
                match index.column():
                    case 0:
                        return self._tasks[index.row()].id
                    case 1:
                        return self._tasks[index.row()].priority
                    case 2:
                        return self._tasks[index.row()].description
                    case 3:
                        if self._tasks[index.row()].recurrence:
                            return str(self._tasks[index.row()].recurrence) + "d"
                    case 4:
                        scheduled = self._tasks[index.row()].scheduled
                        return str(scheduled) if scheduled else ""
                    case 5:
                        deadline = self._tasks[index.row()].deadline
                        return str(deadline) if deadline else ""
                    case 6:
                        return self._tasks[index.row()].days
                    case 7:
                        return duration_to_str(self._tasks[index.row()].average)
                    case 8:
                        return duration_to_str(self._tasks[index.row()].duration)
                    case _:
                        return self._tasks[index.row()].id
            elif role == Qt.BackgroundRole:
                if self._tasks[index.row()] == actions.get_current_task():
                    return QBrush(QColor(0, 255, 0))

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self._tasks)

    def columnCount(self, parent: QModelIndex) -> int:
        return 9

    def refresh(self):
        tasks = Task.select().where(Task.archived == False)
        if self.today:
            tasks = tasks.where(Task.scheduled <= dt.date.today())
        self._tasks = [task for task in tasks]
        self.layoutChanged.emit()

    def done(self, indexes):
        github_token = os.environ.get("GITHUB_TOKEN", "")
        actions.done([str(index.data()) for index in indexes], github_token)
        self.refresh()

    def start(self, index):
        actions.start(str(index.data()), dt.datetime.now(), None)
        self.refresh()

    def stop(self):
        actions.stop()
        self.refresh()
