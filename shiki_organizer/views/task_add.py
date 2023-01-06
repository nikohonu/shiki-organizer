import datetime as dt

from pendulum import duration
from PySide6.QtWidgets import QDialog

from shiki_organizer.views.ui.task_add import Ui_TaskAdd

units = {"days": 1, "weeks": 7, "months": 28, "years": 365}


def get_recurrence_from_number(number):
    if number % 7 == 0:
        return number // 7, "weeks"
    elif number % 28 == 0:
        return number // 84, "months"
    elif number % 365 == 0:
        return number // 365, "years"
    else:
        return number, "days"


def get_duration_from_number(number):
    hours = number // 60
    minutes = number - (hours * 60)
    return hours, minutes


def get_number_from_duration(hours, minutes):
    return hours * 60 + minutes


def get_number_from_recurrence(recurrence, unit):
    return recurrence * units[unit]


class TaskAdd(QDialog, Ui_TaskAdd):
    def __init__(
        self,
        name=None,
        order=None,
        recurrence=None,
        due=None,
        until=None,
        duration_per_day=None,
        notes=None,
    ) -> None:
        super().__init__()
        self.setupUi(self)
        enable_fields = [
            self.order_enable,
            self.recurrence_enable,
            self.due_enable,
            self.until_enable,
            self.duration_per_day_enable,
            self.notes_enable,
        ]
        widgets = [
            [self.order_field],
            [self.recurrence_field, self.unit_field],
            [self.due_field],
            [self.until_field],
            [self.hours_field, self.minutes_field],
            [self.notes_field],
        ]
        for enable_field, fields in zip(enable_fields, widgets):
            f = lambda state, fields=fields: self.change_enable(state, fields)
            enable_field.stateChanged.connect(f)
        if name:
            self.name_field.setText(name)
        if order:
            self.order_field.setValue(order)
            self.order_enable.setChecked(True)
            self.order_enable.stateChanged.emit()
        self.unit_field.addItems(units.keys())
        if recurrence:
            r, u = get_recurrence_from_number(recurrence)
            self.recurrence_field.setValue(r)
            self.unit_field.setCurrentText(u)
            self.recurrence_enable.setChecked(True)
            self.recurrence_enable.stateChanged.emit()
        self.due_field.setDate(dt.date.today())
        if due:
            self.due_field.setDate(due)
            self.due_enable.setChecked(True)
            self.due_enable.stateChanged.emit()
        self.until_field.setDate(dt.date.today())
        if until:
            self.until_field.setDate(until)
            self.until_enable.setChecked(True)
            self.until_enable.stateChanged.emit()
        if duration_per_day:
            h, m = get_duration_from_number(duration_per_day)
            self.hours_field.setValue(h)
            self.minutes_field.setValue(h)
            self.duration_per_day_enable.setChecked(True)
            self.duration_per_day_enable.stateChanged.emit(True)
        if notes:
            self.notes_field.setText(notes)
            self.notes_enable.setChecked(True)
            self.notes_enable.stateChanged.emit()

    def change_enable(self, state, widgets):
        if bool(state):
            for widget in widgets:
                widget.setEnabled(True)
        else:
            for widget in widgets:
                widget.setEnabled(False)

    def result(self):
        name = self.name_field.text()
        order = self.order_field.value() if self.order_enable.isChecked() else None
        recurrence = (
            get_number_from_recurrence(
                self.recurrence_field.value(), self.unit_field.currentText()
            )
            if self.recurrence_enable.isChecked()
            else None
        )
        due = self.due_field.date().toPython() if self.due_enable.isChecked() else None
        until = (
            self.until_field.date().toPython()
            if self.until_enable.isChecked()
            else None
        )
        duration_per_day = (
            get_number_from_duration(
                self.hours_field.value(), self.minutes_field.value()
            )
            if self.duration_per_day_enable.isChecked()
            else None
        )
        notes = self.notes_field.toPlainText() if self.notes_enable.isChecked() else None
        return {
            "name": name,
            "order": order,
            "recurrence": recurrence,
            "due": due,
            "until": until,
            "duration_per_day": duration_per_day,
            "notes": notes,
        }
