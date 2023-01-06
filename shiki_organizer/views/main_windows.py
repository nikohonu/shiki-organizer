from PySide6.QtWidgets import QMainWindow

from shiki_organizer.models.tasks import Tasks
from shiki_organizer.views.task_add import TaskAdd
from shiki_organizer.views.task_tab import TaskTab
from shiki_organizer.views.ui.main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.tab_widget.addTab(TaskTab(), "Task")
        self.action_task_add.triggered.connect(self.add_task)

    def add_task(self):
        task_add = TaskAdd()
        if task_add.exec():
            result = task_add.result()
            if result["name"]:
                tasks = Tasks()
                tasks.add(
                    result["name"],
                    result["order"],
                    result["recurrence"],
                    result["due"],
                    result["until"],
                    result["duration_per_day"],
                    result["notes"],
                )
                print(result)
