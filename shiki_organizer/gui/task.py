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
        self.tasks = Task.select().where(Task.archived == False)
        if self.today:
            self.tasks = self.tasks.where(Task.scheduled <= dt.date.today())
        self.sort_column = 0
        self.sort_order = Qt.SortOrder.DescendingOrder
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
                        return self.tasks[index.row()].id
                    case 1:
                        return self.tasks[index.row()].priority
                    case 2:
                        return self.tasks[index.row()].description
                    case 3:
                        if self.tasks[index.row()].recurrence:
                            return str(self.tasks[index.row()].recurrence) + "d"
                    case 4:
                        scheduled = self.tasks[index.row()].scheduled
                        return str(scheduled) if scheduled else ""
                    case 5:
                        deadline = self.tasks[index.row()].deadline
                        return str(deadline) if deadline else ""
                    case 6:
                        return self.tasks[index.row()].days
                    case 7:
                        return duration_to_str(self.tasks[index.row()].average)
                    case 8:
                        return duration_to_str(self.tasks[index.row()].duration)
            elif role == Qt.BackgroundRole:
                if self.tasks[index.row()] == actions.get_current_task():
                    return QBrush(QColor(0, 255, 0))

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.tasks)

    def columnCount(self, parent: QModelIndex) -> int:
        return 9

    def refresh(self):
        self.tasks = Task.select().where(Task.archived == False)
        if self.today:
            self.tasks = self.tasks.where(Task.scheduled <= dt.date.today())

        def sort_by_any(asc, desc):
            if self.sort_order == Qt.SortOrder.AscendingOrder:
                return asc
            else:
                return desc

        def sort_by_field(asc, desc):
            return sort_by_any(self.tasks.order_by(asc), self.tasks.order_by(desc))

        match self.sort_column:
            case 0:
                self.tasks = sort_by_field(Task.id, Task.id.desc())
            case 1:
                self.tasks = sort_by_field(Task.priority, Task.priority.desc())
            case 2:
                self.tasks = sort_by_field(Task.description, Task.description.desc())
            case 3:
                self.tasks = sort_by_field(Task.recurrence, Task.recurrence.desc())
            case 4:
                self.tasks = sort_by_field(Task.scheduled, Task.scheduled.desc())
            case 5:
                self.tasks = sort_by_field(Task.deadline, Task.deadline.desc())
            case 6:
                self.tasks = sort_by_field(Task.days, Task.days.desc())
            case 7:
                self.tasks = sort_by_any(
                    sorted(self.tasks, key=lambda x: x.average),
                    sorted(self.tasks, key=lambda x: x.average, reverse=True),
                )
            case 8:
                self.tasks = sort_by_field(Task.duration, Task.duration.desc())
        self.layoutChanged.emit()

    def done(self, indexes):
        github_token = os.environ.get("GITHUB_TOKEN", "")
        actions.done([str(index.data()) for index in indexes], github_token)

    def start(self, index):
        actions.start(str(index.data()), dt.datetime.now(), None)

    def stop(self):
        actions.stop()

    def sort(self, column: int, order: Qt.SortOrder) -> None:
        self.sort_column = column
        self.sort_order = order
        self.refresh()
