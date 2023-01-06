# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'task_add.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDateEdit, QDialog, QDialogButtonBox, QGridLayout,
    QLabel, QLineEdit, QSizePolicy, QSpacerItem,
    QSpinBox, QTextEdit, QWidget)

class Ui_TaskAdd(object):
    def setupUi(self, TaskAdd):
        if not TaskAdd.objectName():
            TaskAdd.setObjectName(u"TaskAdd")
        TaskAdd.resize(434, 393)
        self.gridLayout = QGridLayout(TaskAdd)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(TaskAdd)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 7, 0, 1, 1)

        self.label_9 = QLabel(TaskAdd)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 6, 2, 1, 1)

        self.recurrence_field = QSpinBox(TaskAdd)
        self.recurrence_field.setObjectName(u"recurrence_field")
        self.recurrence_field.setEnabled(False)
        self.recurrence_field.setMinimum(1)
        self.recurrence_field.setValue(1)

        self.gridLayout.addWidget(self.recurrence_field, 3, 1, 1, 1)

        self.notes_field = QTextEdit(TaskAdd)
        self.notes_field.setObjectName(u"notes_field")
        self.notes_field.setEnabled(False)

        self.gridLayout.addWidget(self.notes_field, 8, 1, 2, 2)

        self.label_10 = QLabel(TaskAdd)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 2, 2, 1, 1)

        self.label_4 = QLabel(TaskAdd)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.hours_field = QSpinBox(TaskAdd)
        self.hours_field.setObjectName(u"hours_field")
        self.hours_field.setEnabled(False)

        self.gridLayout.addWidget(self.hours_field, 7, 1, 1, 1)

        self.label = QLabel(TaskAdd)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_6 = QLabel(TaskAdd)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.name_field = QLineEdit(TaskAdd)
        self.name_field.setObjectName(u"name_field")

        self.gridLayout.addWidget(self.name_field, 0, 1, 1, 2)

        self.label_3 = QLabel(TaskAdd)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 8, 0, 1, 1)

        self.label_5 = QLabel(TaskAdd)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.notes_enable = QCheckBox(TaskAdd)
        self.notes_enable.setObjectName(u"notes_enable")

        self.gridLayout.addWidget(self.notes_enable, 8, 3, 1, 1)

        self.due_field = QDateEdit(TaskAdd)
        self.due_field.setObjectName(u"due_field")
        self.due_field.setEnabled(False)

        self.gridLayout.addWidget(self.due_field, 4, 1, 1, 2)

        self.due_enable = QCheckBox(TaskAdd)
        self.due_enable.setObjectName(u"due_enable")

        self.gridLayout.addWidget(self.due_enable, 4, 3, 1, 1)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.vertical_spacer, 9, 0, 1, 1)

        self.label_8 = QLabel(TaskAdd)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 6, 1, 1, 1)

        self.order_field = QSpinBox(TaskAdd)
        self.order_field.setObjectName(u"order_field")
        self.order_field.setEnabled(False)
        self.order_field.setMinimum(1)
        self.order_field.setValue(1)

        self.gridLayout.addWidget(self.order_field, 1, 1, 1, 2)

        self.unit_field = QComboBox(TaskAdd)
        self.unit_field.setObjectName(u"unit_field")
        self.unit_field.setEnabled(False)

        self.gridLayout.addWidget(self.unit_field, 3, 2, 1, 1)

        self.until_enable = QCheckBox(TaskAdd)
        self.until_enable.setObjectName(u"until_enable")

        self.gridLayout.addWidget(self.until_enable, 5, 3, 1, 1)

        self.button_box = QDialogButtonBox(TaskAdd)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.button_box, 10, 0, 1, 4)

        self.label_2 = QLabel(TaskAdd)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.until_field = QDateEdit(TaskAdd)
        self.until_field.setObjectName(u"until_field")
        self.until_field.setEnabled(False)

        self.gridLayout.addWidget(self.until_field, 5, 1, 1, 2)

        self.order_enable = QCheckBox(TaskAdd)
        self.order_enable.setObjectName(u"order_enable")

        self.gridLayout.addWidget(self.order_enable, 1, 3, 1, 1)

        self.duration_per_day_enable = QCheckBox(TaskAdd)
        self.duration_per_day_enable.setObjectName(u"duration_per_day_enable")

        self.gridLayout.addWidget(self.duration_per_day_enable, 7, 3, 1, 1)

        self.minutes_field = QSpinBox(TaskAdd)
        self.minutes_field.setObjectName(u"minutes_field")
        self.minutes_field.setEnabled(False)

        self.gridLayout.addWidget(self.minutes_field, 7, 2, 1, 1)

        self.recurrence_enable = QCheckBox(TaskAdd)
        self.recurrence_enable.setObjectName(u"recurrence_enable")

        self.gridLayout.addWidget(self.recurrence_enable, 3, 3, 1, 1)


        self.retranslateUi(TaskAdd)
        self.button_box.accepted.connect(TaskAdd.accept)
        self.button_box.rejected.connect(TaskAdd.reject)

        QMetaObject.connectSlotsByName(TaskAdd)
    # setupUi

    def retranslateUi(self, TaskAdd):
        TaskAdd.setWindowTitle(QCoreApplication.translate("TaskAdd", u"New task", None))
        self.label_7.setText(QCoreApplication.translate("TaskAdd", u"Duration per day:", None))
        self.label_9.setText(QCoreApplication.translate("TaskAdd", u"Minutes", None))
        self.label_10.setText(QCoreApplication.translate("TaskAdd", u"Unit", None))
        self.label_4.setText(QCoreApplication.translate("TaskAdd", u"Recurrence:", None))
        self.label.setText(QCoreApplication.translate("TaskAdd", u"Name:", None))
        self.label_6.setText(QCoreApplication.translate("TaskAdd", u"Until:", None))
        self.label_3.setText(QCoreApplication.translate("TaskAdd", u"Notes:", None))
        self.label_5.setText(QCoreApplication.translate("TaskAdd", u"Due:", None))
        self.notes_enable.setText(QCoreApplication.translate("TaskAdd", u"Enable", None))
        self.due_field.setDisplayFormat(QCoreApplication.translate("TaskAdd", u"yyyy-MM-dd", None))
        self.due_enable.setText(QCoreApplication.translate("TaskAdd", u"Enable", None))
        self.label_8.setText(QCoreApplication.translate("TaskAdd", u"Hours", None))
        self.until_enable.setText(QCoreApplication.translate("TaskAdd", u"Enable", None))
        self.label_2.setText(QCoreApplication.translate("TaskAdd", u"Order:", None))
        self.until_field.setDisplayFormat(QCoreApplication.translate("TaskAdd", u"yyyy-MM-dd", None))
        self.order_enable.setText(QCoreApplication.translate("TaskAdd", u"Enable", None))
        self.duration_per_day_enable.setText(QCoreApplication.translate("TaskAdd", u"Enable", None))
        self.recurrence_enable.setText(QCoreApplication.translate("TaskAdd", u"Enable", None))
    # retranslateUi

