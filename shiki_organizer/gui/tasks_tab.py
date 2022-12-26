import datetime as dt
import string

from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QDialog, QWidget

from shiki_organizer.gui.task import TaskTableModel
from shiki_organizer.gui.ui.task_add import Ui_TaskAdd
from shiki_organizer.gui.ui.tasks_tab import Ui_TaskTab
from shiki_organizer.gui.ui_helper import shortcut_button_connect
from shiki_organizer.model import Task


class TaskAdd(QDialog, Ui_TaskAdd):
    def __init__(
        self,
        description=None,
        priority=None,
        recurrence=None,
        scheduled=None,
        deadline=None,
        parent_task=None,
    ) -> None:
        super().__init__()
        self.setupUi(self)
        self.tasks = list(
            Task.select().where(Task.archived == False).order_by(Task.description)
        )
        self.priority.addItems(list(string.ascii_uppercase))
        if description:
            self.description.setText(description)
        if priority:
            self.priority.setCurrentIndex(list(string.ascii_uppercase).index(priority))
            self.has_prioirty.setChecked(True)
            self.on_has_prioirty_checked(True)
        if recurrence:
            self.recurrence.setValue(recurrence)
            self.has_recurrence.setChecked(True)
            self.on_has_recurrence_checked(True)
        if scheduled:
            self.scheduled.setDate(scheduled)
            self.has_scheduled.setChecked(True)
            self.on_has_scheduled_checked(True)
        else:
            self.scheduled.setDateTime(dt.datetime.now())
        if deadline:
            self.deadline.setDate(deadline)
            self.has_deadline.setChecked(True)
            self.on_has_deadline_checked(True)
        else:
            self.deadline.setDateTime(dt.datetime.now() + dt.timedelta(days=28))
        self.parent_task.addItems([task.description for task in self.tasks])
        if parent_task:
            self.parent_task.setCurrentIndex(self.tasks.index(parent_task))
            self.has_parent_task.setChecked(True)
            self.on_has_parent_task_checked(True)
        self.has_prioirty.stateChanged.connect(self.on_has_prioirty_checked)
        self.has_recurrence.stateChanged.connect(self.on_has_recurrence_checked)
        self.has_scheduled.stateChanged.connect(self.on_has_scheduled_checked)
        self.has_deadline.stateChanged.connect(self.on_has_deadline_checked)
        self.has_parent_task.stateChanged.connect(self.on_has_parent_task_checked)

    def on_has_checked(self, has, widget):
        if bool(has):
            widget.setEnabled(True)
        else:
            widget.setEnabled(False)

    def on_has_prioirty_checked(self, has_prioirty):
        self.on_has_checked(has_prioirty, self.priority)

    def on_has_recurrence_checked(self, has_recurrence):
        self.on_has_checked(has_recurrence, self.recurrence)

    def on_has_scheduled_checked(self, has_scheduled):
        self.on_has_checked(has_scheduled, self.scheduled)

    def on_has_deadline_checked(self, has_deadline):
        self.on_has_checked(has_deadline, self.deadline)

    def on_has_parent_task_checked(self, has_parent_task):
        self.on_has_checked(has_parent_task, self.parent_task)

    def result(self):
        description = self.description.text()
        priority = (
            self.priority.currentText() if self.has_prioirty.isChecked() else None
        )
        recurrence = (
            self.recurrence.value() if self.has_recurrence.isChecked() else None
        )
        scheduled = (
            self.scheduled.date().toPython() if self.has_scheduled.isChecked() else None
        )
        deadline = (
            self.deadline.date().toPython() if self.has_deadline.isChecked() else None
        )
        parent_task = (
            self.tasks[self.parent_task.currentIndex()]
            if self.has_parent_task.isChecked()
            else None
        )
        return description, priority, recurrence, scheduled, deadline, parent_task


class TasksTab(QWidget, Ui_TaskTab):
    def __init__(self, today: bool = True):
        super(TasksTab, self).__init__()
        self.setupUi(self)
        self.model = TaskTableModel(today)
        self.view.setModel(self.model)
        self.shortcut_done = QShortcut(QKeySequence("C"), self)
        self.shortcut_start = QShortcut(QKeySequence("S"), self)
        self.shortcut_stop = QShortcut(QKeySequence("Q"), self)
        self.shortcut_add = QShortcut(QKeySequence("A"), self)
        self.shortcut_delete = QShortcut(QKeySequence("D"), self)
        self.shortcut_modify = QShortcut(QKeySequence("E"), self)
        shortcut_button_connect(self.shortcut_done, self.button_done, self.done)
        shortcut_button_connect(self.shortcut_start, self.button_start, self.start)
        shortcut_button_connect(self.shortcut_stop, self.button_stop, self.stop)
        shortcut_button_connect(self.shortcut_add, self.button_add, self.add)
        shortcut_button_connect(self.shortcut_delete, self.button_delete, self.delete)
        shortcut_button_connect(self.shortcut_modify, self.button_modify, self.modify)

    def get_selected_interval(self):
        selected_rows = self.view.selectionModel().selectedRows()
        if len(selected_rows) == 0:
            return
        if len(selected_rows) > 1:
            self.view.selectRow(selected_rows[0].row())
        if selected_rows[0]:
            return Task.get_by_id(selected_rows[0].data())
        else:
            return None

    def done(self):
        self.model.done(self.view.selectionModel().selectedRows())
        self.view.selectionModel().clearSelection()

    def start(self):
        self.model.start(self.view.selectionModel().selectedRows()[0])
        self.view.selectionModel().clearSelection()

    def stop(self):
        self.model.stop()

    def add(self):
        task_add = TaskAdd()
        if task_add.exec():
            (
                description,
                priority,
                recurrence,
                scheduled,
                deadline,
                parent,
            ) = task_add.result()
            task = Task.create(
                description=description,
                priority=priority,
                recurrence=recurrence,
                scheduled=scheduled,
                deadline=deadline,
                parent=parent,
            )
            Task.reindex()
            self.model.refresh()

    def modify(self):
        task = self.get_selected_interval()
        if task:
            task_add = TaskAdd(
                task.description,
                task.priority,
                task.recurrence,
                task.scheduled,
                task.deadline,
                task.parent,
            )
            if task_add.exec():
                (
                    description,
                    priority,
                    recurrence,
                    scheduled,
                    deadline,
                    parent,
                ) = task_add.result()
                q = task.update(
                    description=description,
                    priority=priority,
                    recurrence=recurrence,
                    scheduled=scheduled,
                    deadline=deadline,
                    parent=parent,
                ).where(Task.id == task.id)
                q.execute()
                self.model.refresh()

    def delete(self):
        task = self.get_selected_interval()
        if task:
            task.delete_instance()
            self.model.refresh()
