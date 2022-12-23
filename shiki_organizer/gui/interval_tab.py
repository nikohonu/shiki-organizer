from PySide6.QtWidgets import QWidget, QHeaderView, QDialog
from shiki_organizer.gui.ui.interval_tab import Ui_IntervalTab
from shiki_organizer.gui.ui.interval_modify import Ui_IntervalModify
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, Signal, QTimer

from shiki_organizer.model import Interval, Task
from shiki_organizer.formatter import duration_to_str, datetime_to_str
import datetime as dt
from shiki_organizer.datetime import period_to_datetime


class IntervalModify(QDialog, Ui_IntervalModify):
    def __init__(self, task, start, end) -> None:
        super(IntervalModify, self).__init__()
        self.setupUi(self)
        self.start.setDateTime(start)
        if not end:
            self.end_none.setChecked(True)
            self.end.setDateTime(dt.datetime.now())
            self.end.setEnabled(False)
        else:
            self.end.setDateTime(end)
        self.end_none.stateChanged.connect(self.enable_disable_end)
        self.tasks = list(Task.select())
        self.task.addItems([task.description for task in self.tasks])
        self.task.setCurrentIndex(self.tasks.index(task))

    def enable_disable_end(self, state):
        self.end.setEnabled(not bool(state))

    def get_start(self):
        return self.start.dateTime().toPython()

    def get_end(self):
        if self.end_none.isChecked():
            return None
        else:
            return self.end.dateTime().toPython()

    @property
    def current_task(self):
        return self.tasks[self.task.currentIndex()]


class IntervalModel(QAbstractTableModel):
    total_duration_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._start = dt.datetime.min
        self._intervals = Interval.select().where(Interval.start >= self._start)
        self._headers = ["ID", "Task description", "Start", "End", "Duration"]
        self.total_duration_changed.emit(self.get_total_duration())

        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(
            lambda: self.total_duration_changed.emit(self.get_total_duration())
        )
        timer.start()

    def columnCount(self, parent: QModelIndex) -> int:
        return 5

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self._intervals)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if orientation == Qt.Orientation.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return super().headerData(section, orientation, role)

    def data(self, index: QModelIndex, role: int):
        if index.isValid():
            if role == Qt.DisplayRole:
                interval = self._intervals[index.row()]
                match index.column():
                    case 0:
                        return interval.id
                    case 1:
                        return interval.task.description
                    case 2:
                        return datetime_to_str(interval.start)
                    case 3:
                        return datetime_to_str(interval.end) if interval.end else ""
                    case _:
                        return duration_to_str(interval.duration)

    def get_total_duration(self):
        total_duration = 0
        for interval in self._intervals:
            total_duration += interval.duration
        return total_duration

    def change_period(self, period):
        self._start = period_to_datetime(period)
        self.refresh()

    def refresh(self):
        self._intervals = Interval.select().where(Interval.start >= self._start)
        self.dataChanged.emit(1, 1)
        self.headerDataChanged.emit(Qt.Orientation.Vertical, 1, 1)

    def modify(self, index):
        interval = Interval.get_by_id(index.data())
        interval_modify = IntervalModify(interval.task, interval.start, interval.end)
        if interval_modify.exec():
            q = interval.update(
                task=interval_modify.current_task,
                start=interval_modify.get_start(),
                end=interval_modify.get_end(),
            ).where(Interval.id == interval.id)
            q.execute()
            self.refresh()
        # actions.start(str(index.data()), dt.datetime.now(), None)
        # self.refresh()


class IntervalTab(QWidget, Ui_IntervalTab):
    def __init__(self):
        super(IntervalTab, self).__init__()
        self.setupUi(self)
        self.model = IntervalModel()
        self.view.setModel(self.model)
        self.view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.view.verticalHeader().hide()
        self.on_total_duration_changed(self.model.get_total_duration())
        self.model.total_duration_changed.connect(self.on_total_duration_changed)
        self.period.currentTextChanged.connect(self.model.change_period)

        self.button_modify.clicked.connect(self.modify)

    def on_total_duration_changed(self, total_duration):
        self.status.setText(f"Total duration: {duration_to_str(total_duration)}")

    def modify(self):
        selected_rows = self.view.selectionModel().selectedRows()
        if len(selected_rows) == 0:
            return
        if len(selected_rows) > 1:
            self.view.selectRow(selected_rows[0].row())
        self.model.modify(selected_rows[0])
