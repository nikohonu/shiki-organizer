import sys

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QMainWindow

from shiki_organizer.gui.interval_tab import IntervalTab
from shiki_organizer.gui.repository_tab import RepositoryTab
from shiki_organizer.gui.settings_tab import SettingsTab
from shiki_organizer.gui.tasks_tab import TasksTab
from shiki_organizer.gui.ui.main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    update_all = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tab_widget.addTab(TasksTab(self.update_all, True), "Today")
        self.tab_widget.addTab(TasksTab(self.update_all, False), "Tasks")
        self.tab_widget.addTab(IntervalTab(self.update_all), "Intervals")
        self.tab_widget.addTab(RepositoryTab(), "Repository")
        self.tab_widget.addTab(SettingsTab(), "Settings")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
