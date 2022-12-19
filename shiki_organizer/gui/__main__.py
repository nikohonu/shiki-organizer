import os
import random
import shutil
import subprocess
import sys

from peewee import fn
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QSizePolicy
)
from PySide6.QtGui import QPixmap, QResizeEvent, QShortcut, QKeySequence
from PySide6.QtCore import Qt
from shiki_organizer.gui.task import TaskTableModel
from shiki_organizer.gui.ui.main_window import Ui_MainWindow

# class TasksWidegt(QWidget):
#     def __init__(self, parent=None) -> None:
#         super().__init__(parent)
#         self.main_layout = QVBoxLayout()
#         self.header_layout = QHBoxLayout()
#         self.footer_layout = QHBoxLayout()

#         self.view = QtWidgets.QTableView()
#         self.model = TaskTableModel()
#         self.view.setModel(self.model)
#         self.today = QCheckBox("Show only today task")
#         self.do_button = QPushButton("Do")
#         self.today.stateChanged.connect(self.toggle_today)
#         self.do_button.clicked.connect(self.do)

#         self.header_layout.addWidget(self.today)
#         self.footer_layout.addWidget(self.do_button)
#         self.main_layout.addLayout(self.header_layout)
#         self.main_layout.addWidget(self.view)
#         self.main_layout.addLayout(self.footer_layout)
#         self.setLayout(self.main_layout)

#     def toggle_today(self, state):
#         self.model.toggle_today(state)

#     def do(self):
#         self.model.do(self.view.selectionModel().selectedIndexes())


# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.resize(900, 500)
#         self.setCentralWidget(TasksWidegt())

#         # self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

#         # self.button = QtWidgets.QPushButton("Click me!")
#         # self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

#         # self.layout = QtWidgets.QVBoxLayout(self)
#         # self.setCentralWidget(self.layout)
#         # self.layout.addWidget(self.text)
#         # self.layout.addWidget(self.button)

#         # self.button.clicked.connect(self.magic)
#         # self.setCentralWidget(self.button)

#     # @QtCore.Slot()
#     # def magic(self):
#     # self.text.setText(random.choice(self.hello))

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.model = TaskTableModel()
        self.view.setModel(self.model)
        self.shortcut_done = QShortcut(QKeySequence('C'), self)
        self.shortcut_start = QShortcut(QKeySequence('S'), self)
        self.shortcut_stop = QShortcut(QKeySequence('Q'), self)
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

def main():
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
