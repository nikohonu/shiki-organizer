import datetime as dt

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QTimer, Signal
from PySide6.QtWidgets import QDialog, QHeaderView, QMessageBox, QWidget

import shiki_organizer.actions as actions
from shiki_organizer.datetime import period_to_datetime
from shiki_organizer.formatter import datetime_to_str, duration_to_str
from shiki_organizer.gui.ui.repository_add import Ui_RepositoryAdd
from shiki_organizer.gui.ui.repository_tab import Ui_RepositoryTab
from shiki_organizer.model import Interval, Repository, Task


class RepositoryAdd(QDialog, Ui_RepositoryAdd):
    def __init__(self, name=None, parent=None) -> None:
        super().__init__()
        self.setupUi(self)
        self.tasks = list(Task.select().order_by(Task.description))
        self.task.addItems([task.description for task in self.tasks])
        if parent:
            self.task.setCurrentIndex(self.tasks.index(parent))
        if name:
            self.name.setText(name)

    def result(self):
        name = self.name.text()
        parent = self.tasks[self.task.currentIndex()]
        return name, parent


class RepositoryModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.sort_column = 0
        self.sort_order = Qt.SortOrder.DescendingOrder
        self.headers = ["ID", "Name", "Task description"]
        self.refresh()

    def columnCount(self, parent: QModelIndex) -> int:
        return 3

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.repositories)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if orientation == Qt.Orientation.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return super().headerData(section, orientation, role)

    def data(self, index: QModelIndex, role: int):
        if index.isValid():
            if role == Qt.DisplayRole:
                repository = self.repositories[index.row()]
                match index.column():
                    case 0:
                        return repository.id
                    case 1:
                        return repository.name
                    case 2:
                        return repository.parent.description

    def refresh(self):
        self.repositories = Repository.select().join(Task)
        match self.sort_column:
            case 0:
                if self.sort_order == Qt.SortOrder.AscendingOrder:
                    self.repositories = self.repositories.order_by(Repository.id)
                else:
                    self.repositories = self.repositories.order_by(Repository.id.desc())
            case 1:
                if self.sort_order == Qt.SortOrder.AscendingOrder:
                    self.repositories = self.repositories.order_by(Repository.name)
                else:
                    self.repositories = self.repositories.order_by(
                        Repository.name.desc()
                    )
            case 2:
                if self.sort_order == Qt.SortOrder.AscendingOrder:
                    self.repositories = self.repositories.order_by(Task.description)
                else:
                    self.repositories = self.repositories.order_by(
                        Task.description.desc()
                    )
        self.layoutChanged.emit()

    def sort(self, column: int, order: Qt.SortOrder) -> None:
        self.sort_column = column
        self.sort_order = order
        self.refresh()


class RepositoryTab(QWidget, Ui_RepositoryTab):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.model = RepositoryModel()
        self.view.setModel(self.model)
        self.view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        self.button_modify.clicked.connect(self.modify)
        self.button_add.clicked.connect(self.add)
        self.button_delete.clicked.connect(self.delete)
        self.button_pull.clicked.connect(self.pull)

    def get_selected_repository(self):
        selected_rows = self.view.selectionModel().selectedRows()
        if len(selected_rows) == 0:
            return
        if len(selected_rows) > 1:
            self.view.selectRow(selected_rows[0].row())
        if selected_rows[0]:
            return Repository.get_by_id(selected_rows[0].data())
        else:
            return None

    def modify(self):
        repository = self.get_selected_repository()
        if repository:
            repository_modify = RepositoryAdd(repository.name, repository.parent)
            repository_modify.setWindowTitle("Modify repository")
            if repository_modify.exec():
                name, parent = repository_modify.result()
                q = repository.update(name=name, parent=parent).where(
                    Repository.id == repository.id
                )
                q.execute()
                self.model.refresh()

    def add(self):
        repository_add = RepositoryAdd()
        if repository_add.exec():
            name, parent = repository_add.result()
            Repository.create(name=name, parent=parent)
            Repository.reindex()
            self.model.refresh()

    def delete(self):
        repository = self.get_selected_repository()
        if repository:
            repository.delete_instance()
            self.model.refresh()


    def pull(self):
        message = actions.pull()
        if message:
            QMessageBox.about(self, "Pull issue", message)
