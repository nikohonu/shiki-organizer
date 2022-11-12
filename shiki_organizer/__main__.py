import random
import sys

from PySide6 import QtCore, QtGui, QtWidgets

from shiki_organizer.task import TaskTableModel


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(900, 500)
        self.view = QtWidgets.QTableView()
        self.model = TaskTableModel()
        self.view.setModel(self.model)
        self.setCentralWidget(self.view)

        #self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        #self.button = QtWidgets.QPushButton("Click me!")
        #self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        #self.layout = QtWidgets.QVBoxLayout(self)
        # self.setCentralWidget(self.layout)
        #self.layout.addWidget(self.text)
        #self.layout.addWidget(self.button)

        #self.button.clicked.connect(self.magic)
        #self.setCentralWidget(self.button)

    #@QtCore.Slot()
    #def magic(self):
        #self.text.setText(random.choice(self.hello))


def main():
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
