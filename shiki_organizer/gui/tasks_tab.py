from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QShortcut, QKeySequence
from shiki_organizer.gui.task import TaskTableModel
from shiki_organizer.gui.ui.tasks_tab import Ui_TaskTab


class TasksTab(QWidget, Ui_TaskTab):
    def __init__(self, today: bool = True):
        super(TasksTab, self).__init__()
        self.setupUi(self)
        self.model = TaskTableModel(today)
        self.view.setModel(self.model)
        self.shortcut_done = QShortcut(QKeySequence("C"), self)
        self.shortcut_start = QShortcut(QKeySequence("S"), self)
        self.shortcut_stop = QShortcut(QKeySequence("Q"), self)
        self.shortcut_done.activated.connect(self.done)
        self.shortcut_start.activated.connect(self.start)
        self.shortcut_stop.activated.connect(self.stop)
        self.button_done.clicked.connect(self.done)
        self.button_start.clicked.connect(self.start)
        self.button_stop.clicked.connect(self.stop)

    def done(self):
        self.model.done(self.view.selectionModel().selectedRows())
        self.view.selectionModel().clearSelection()

    def start(self):
        self.model.start(self.view.selectionModel().selectedRows()[0])
        self.view.selectionModel().clearSelection()

    def stop(self):
        self.model.stop()
