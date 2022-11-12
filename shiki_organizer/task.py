from PySide6.QtCore import QAbstractListModel, QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QLabel

from shiki_organizer.model import Task


class TaskTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._tasks = [task for task in Task.select()]

    def data(self, index: QModelIndex, role: int):
        print(role)
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self._tasks[index.row()].id
            elif index.column() == 1:
                return self._tasks[index.row()].description
            elif index.column() == 2:
                if self._tasks[index.row()].recurrence:
                    return str(self._tasks[index.row()].recurrence) + "d"
            else:
                return str(self._tasks[index.row()].scheduled)

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self._tasks)

    def columnCount(self, parent: QModelIndex) -> int:
        return 4
