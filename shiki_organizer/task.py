from datetime import date, datetime, timedelta

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, Signal
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QLabel

from shiki_organizer.commands.stop_command import run_stop_command
from shiki_organizer.model import Task


class TaskTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._tasks = [task for task in Task.select()]
        self._headers = ["Name", "Recurrence", "Due"]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if orientation == Qt.Orientation.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        if orientation == Qt.Orientation.Vertical and role == Qt.DisplayRole:
            return self._tasks[section].id
        return super().headerData(section, orientation, role)

    def data(self, index: QModelIndex, role: int):
        if role == Qt.DisplayRole:
            match index.column():
                case 0:
                    return self._tasks[index.row()].description
                case 1:
                    if self._tasks[index.row()].recurrence:
                        return str(self._tasks[index.row()].recurrence) + "d"
                case _:
                    return str(self._tasks[index.row()].scheduled)

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self._tasks)

    def columnCount(self, parent: QModelIndex) -> int:
        return 3

    def refresh(self):
        self.dataChanged.emit(1, 1)
        self.headerDataChanged.emit(Qt.Orientation.Vertical, 1, 1)

    def toggle_today(self, state):
        if state:
            self._tasks = [
                task for task in Task.select().where(Task.scheduled == date.today())
            ]
        else:
            self._tasks = [task for task in Task.select()]
        self.refresh()

    def do(self, indexes: list):
        for row in set([index.row() for index in indexes]):
            task = self._tasks[row]
            if task.recurrence:
                task.scheduled = (
                    datetime.now() + timedelta(days=task.recurrence)
                ).date()
                if task.deadline and task.scheduled > task.deadline:
                    task.is_completed = True
                    task.scheduled = datetime.now()
            else:
                task.is_completed = True
            task.save()
            run_stop_command()
        self.refresh()
