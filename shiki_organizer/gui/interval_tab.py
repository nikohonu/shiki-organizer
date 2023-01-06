import datetime as dt

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QTimer, Signal
from PySide6.QtWidgets import QDialog, QHeaderView, QWidget

from shiki_organizer.datetime import period_to_datetime
from shiki_organizer.formatter import datetime_to_str, duration_to_str
from shiki_organizer.gui.ui.interval_add import Ui_IntervalAdd
from shiki_organizer.gui.ui.interval_tab import Ui_IntervalTab
from shiki_organizer.database import Interval, Task


class IntervalAdd(QDialog, Ui_IntervalAdd):
    def __init__(
        self, start: dt.datetime, end: dt.datetime = None, task: Task = None
    ) -> None:
        super(IntervalAdd, self).__init__()
        self.setupUi(self)
        self.tasks = list(Task.select().order_by(Task.description))
        self.task.addItems([task.description for task in self.tasks])
        if task:
            self.task.setCurrentIndex(self.tasks.index(task))
        self.date.setDate(start.date())
        self.start.setDateTime(start)
        if end:
            self.end.setDateTime(end)
        else:
            self.end.setDateTime(dt.datetime.now())
            self.has_end.setChecked(False)
            self.set_end(False)
        self.calc_duration()
        self.start.timeChanged.connect(self.calc_duration)
        self.end.timeChanged.connect(self.calc_duration)
        self.date.dateChanged.connect(self.calc_duration)
        self.duration.timeChanged.connect(self.calc_end)
        self.has_end.stateChanged.connect(self.set_end)

    def set_end(self, has_end):
        if bool(has_end):
            self.end.setEnabled(True)
            self.duration.setEnabled(True)
        else:
            self.end.setEnabled(False)
            self.duration.setEnabled(False)

    def calc_duration(self):
        date = self.date.date().toPython()
        start = dt.datetime.combine(date, self.start.time().toPython())
        end = dt.datetime.combine(date, self.end.time().toPython())
        if start < end:
            duration = end - start
            self.start.setDateTime(start)
            self.end.setDateTime(end)
            self.duration.setDateTime(dt.datetime.combine(date, dt.time.min) + duration)

    def calc_end(self):
        date = self.date.date().toPython()
        start = dt.datetime.combine(date, self.start.time().toPython())
        duration = self.duration.dateTime().toPython() - dt.datetime.combine(
            date, dt.time.min
        )
        end = start + duration
        self.end.setDateTime(end)

    def result(self):
        task = self.tasks[self.task.currentIndex()]
        start = self.start.dateTime().toPython()
        end = self.end.dateTime().toPython() if self.has_end.isChecked() else None
        return task, start, end


class IntervalModel(QAbstractTableModel):
    total_duration_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.start = dt.datetime.min
        self.sort_column = 0
        self.sort_order = Qt.SortOrder.DescendingOrder
        self.headers = ["ID", "Task description", "Start", "End", "Duration"]
        self.refresh()
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
        return len(self.intervals)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if orientation == Qt.Orientation.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return super().headerData(section, orientation, role)

    def data(self, index: QModelIndex, role: int):
        if index.isValid():
            if role == Qt.DisplayRole:
                interval = self.intervals[index.row()]
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
        for interval in self.intervals:
            total_duration += interval.duration
        return total_duration

    def change_period(self, period):
        self.start = period_to_datetime(period)
        self.refresh()

    def refresh(self):
        self.intervals = (
            Interval.select().join(Task).where(Interval.start >= self.start)
        )
        match self.sort_column:
            case 0:
                if self.sort_order == Qt.SortOrder.AscendingOrder:
                    self.intervals = self.intervals.order_by(Interval.id)
                else:
                    self.intervals = self.intervals.order_by(Interval.id.desc())
            case 1:
                if self.sort_order == Qt.SortOrder.AscendingOrder:
                    self.intervals = self.intervals.order_by(Task.description)
                else:
                    self.intervals = self.intervals.order_by(Task.description.desc())
            case 2:
                if self.sort_order == Qt.SortOrder.AscendingOrder:
                    self.intervals = self.intervals.order_by(Interval.start)
                else:
                    self.intervals = self.intervals.order_by(Interval.start.desc())
            case 3:
                if self.sort_order == Qt.SortOrder.AscendingOrder:
                    self.intervals = self.intervals.order_by(Interval.end)
                else:
                    self.intervals = self.intervals.order_by(Interval.end.desc())
            case 4:
                if self.sort_order == Qt.SortOrder.AscendingOrder:
                    self.intervals = sorted(self.intervals, key=lambda x: x.duration)
                else:
                    self.intervals = sorted(
                        self.intervals, key=lambda x: x.duration, reverse=True
                    )
        self.layoutChanged.emit()

    def sort(self, column: int, order: Qt.SortOrder) -> None:
        self.sort_column = column
        self.sort_order = order
        self.refresh()


class IntervalTab(QWidget, Ui_IntervalTab):
    def __init__(
        self,
        update_all: Signal,
    ):
        super(IntervalTab, self).__init__()
        self.setupUi(self)
        self.update_all = update_all
        self.model = IntervalModel()
        self.update_all.connect(self.model.refresh)
        self.view.setModel(self.model)
        self.view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.view.verticalHeader().hide()
        self.on_total_duration_changed(self.model.get_total_duration())
        self.model.total_duration_changed.connect(self.on_total_duration_changed)
        self.period.currentTextChanged.connect(self.model.change_period)

        self.button_modify.clicked.connect(self.modify)
        self.button_add.clicked.connect(self.add)
        self.button_delete.clicked.connect(self.delete)

    def on_total_duration_changed(self, total_duration):
        self.status.setText(f"Total duration: {duration_to_str(total_duration)}")

    def get_selected_interval(self):
        selected_rows = self.view.selectionModel().selectedRows()
        if len(selected_rows) == 0:
            return
        if len(selected_rows) > 1:
            self.view.selectRow(selected_rows[0].row())
        if selected_rows[0]:
            return Interval.get_by_id(selected_rows[0].data())
        else:
            return None

    def modify(self):
        interval = self.get_selected_interval()
        if interval:
            interval_modify = IntervalAdd(interval.start, interval.end, interval.task)
            interval_modify.setWindowTitle("Modify interval")
            if interval_modify.exec():
                task, start, end = interval_modify.result()
                q = interval.update(
                    task=task,
                    start=start,
                    end=end,
                ).where(Interval.id == interval.id)
                q.execute()
                self.model.refresh()

    def add(self):
        interval = self.get_selected_interval()
        task = interval.task if interval else None
        interval_add = IntervalAdd(
            dt.datetime.now(), dt.datetime.now() + dt.timedelta(minutes=5)
        )
        if interval_add.exec():
            task, start, end = interval_add.result()
            Interval.create(task=task, start=start, end=end)
            Interval.reindex()
            self.model.refresh()

    def delete(self):
        interval = self.get_selected_interval()
        if interval:
            interval.delete_instance()
            self.model.refresh()
