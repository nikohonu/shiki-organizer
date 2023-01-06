from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QApplication

from shiki_organizer.models import tasks
from shiki_organizer.models.tasks import Tasks


class TaskTable(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        # self.tasks = QApplication.instance().tasks
        self.tasks = Tasks()
        self.tasks.updated.connect(self.layoutChanged.emit)

    def rowCount(self, parent=None):
        return len(self.tasks)

    def columnCount(self, parent=None):
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row() + 1
            column = index.column() + 1
            return self.tasks[index.row()]
        return None
