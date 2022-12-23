import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from shiki_organizer.gui.ui.main_window import Ui_MainWindow
from shiki_organizer.gui.tasks_tab import TasksTab
from shiki_organizer.gui.interval_tab import IntervalTab


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.tab_widget.addTab(TasksTab(True), "Today")
        self.tab_widget.addTab(TasksTab(False), "Tasks")
        self.tab_widget.addTab(IntervalTab(), "Intervals")


def main():
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
