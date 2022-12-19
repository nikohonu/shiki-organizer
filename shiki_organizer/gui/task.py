# from datetime import date, datetime, timedelta

import os
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, Signal

from PySide6.QtGui import QBrush, QColor

# from PySide6.QtWidgets import QLabel

# from shiki_organizer.commands.stop_command import run_stop_command
from shiki_organizer.model import Task
import shiki_organizer.actions as actions
import datetime as dt


class TaskTableModel(QAbstractTableModel):
    def __init__(self, parent=None, today=False):
        super().__init__(parent)

        self._tasks = [
            task for task in Task.select().where(Task.scheduled <= dt.date.today())
        ]
        self._headers = ["ID", "Name", "Recurrence", "Due"]

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
                        return self._tasks[index.row()].description
                    case 2:
                        if self._tasks[index.row()].recurrence:
                            return str(self._tasks[index.row()].recurrence) + "d"
                    case _:
                        return str(self._tasks[index.row()].scheduled)
            elif role == Qt.BackgroundRole:
                if self._tasks[index.row()] == actions.get_current_task():
                    return QBrush(QColor(0, 255, 0))

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self._tasks)

    def columnCount(self, parent: QModelIndex) -> int:
        return 4

    def refresh(self):
        self._tasks = [
            task for task in Task.select().where(Task.scheduled <= dt.date.today())
        ]
        self.dataChanged.emit(1, 1)
        self.headerDataChanged.emit(Qt.Orientation.Vertical, 1, 1)

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
