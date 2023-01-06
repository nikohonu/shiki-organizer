from PySide6.QtWidgets import QWidget

from shiki_organizer.models.task_table import TaskTable
from shiki_organizer.views.ui.tasks_tab import Ui_TaskTab


class TaskTab(QWidget, Ui_TaskTab):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.model = TaskTable()
        self.view.setModel(self.model)


