import random
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from shiki_organizer.task import TaskTableModel


class TasksWidegt(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.main_layout = QVBoxLayout()
        self.header_layout = QHBoxLayout()
        self.footer_layout = QHBoxLayout()

        self.view = QtWidgets.QTableView()
        self.model = TaskTableModel()
        self.view.setModel(self.model)
        self.today = QCheckBox("Show only today task")
        self.do_button = QPushButton("Do")
        self.today.stateChanged.connect(self.toggle_today)
        self.do_button.clicked.connect(self.do)

        self.header_layout.addWidget(self.today)
        self.footer_layout.addWidget(self.do_button)
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addWidget(self.view)
        self.main_layout.addLayout(self.footer_layout)
        self.setLayout(self.main_layout)

    def toggle_today(self, state):
        self.model.toggle_today(state)

    def do(self):
        self.model.do(self.view.selectionModel().selectedIndexes())


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(900, 500)
        self.setCentralWidget(TasksWidegt())

        # self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        # self.button = QtWidgets.QPushButton("Click me!")
        # self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        # self.layout = QtWidgets.QVBoxLayout(self)
        # self.setCentralWidget(self.layout)
        # self.layout.addWidget(self.text)
        # self.layout.addWidget(self.button)

        # self.button.clicked.connect(self.magic)
        # self.setCentralWidget(self.button)

    # @QtCore.Slot()
    # def magic(self):
    # self.text.setText(random.choice(self.hello))


def main():
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
