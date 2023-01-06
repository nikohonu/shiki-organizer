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
    QSpinBox, QWidget)

class Ui_TaskAdd(object):
    def setupUi(self, TaskAdd):
        if not TaskAdd.objectName():
            TaskAdd.setObjectName(u"TaskAdd")
        TaskAdd.resize(398, 314)
        self.gridLayout = QGridLayout(TaskAdd)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(TaskAdd)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 8, 1, 1, 3)

        self.has_prioirty = QCheckBox(TaskAdd)
        self.has_prioirty.setObjectName(u"has_prioirty")

        self.gridLayout.addWidget(self.has_prioirty, 1, 3, 1, 1)

        self.deadline = QDateEdit(TaskAdd)
        self.deadline.setObjectName(u"deadline")
        self.deadline.setEnabled(False)

        self.gridLayout.addWidget(self.deadline, 4, 2, 1, 1)

        self.description = QLineEdit(TaskAdd)
        self.description.setObjectName(u"description")

        self.gridLayout.addWidget(self.description, 0, 2, 1, 1)

        self.label_3 = QLabel(TaskAdd)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)

        self.has_deadline = QCheckBox(TaskAdd)
        self.has_deadline.setObjectName(u"has_deadline")

        self.gridLayout.addWidget(self.has_deadline, 4, 3, 1, 1)

        self.recurrence = QSpinBox(TaskAdd)
        self.recurrence.setObjectName(u"recurrence")
        self.recurrence.setEnabled(False)
        self.recurrence.setMinimum(1)
        self.recurrence.setMaximum(9999)

        self.gridLayout.addWidget(self.recurrence, 2, 2, 1, 1)

        self.has_scheduled = QCheckBox(TaskAdd)
        self.has_scheduled.setObjectName(u"has_scheduled")

        self.gridLayout.addWidget(self.has_scheduled, 3, 3, 1, 1)

        self.has_parent_task = QCheckBox(TaskAdd)
        self.has_parent_task.setObjectName(u"has_parent_task")

        self.gridLayout.addWidget(self.has_parent_task, 6, 3, 1, 1)

        self.label = QLabel(TaskAdd)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.label_2 = QLabel(TaskAdd)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.priority = QComboBox(TaskAdd)
        self.priority.setObjectName(u"priority")
        self.priority.setEnabled(False)

        self.gridLayout.addWidget(self.priority, 1, 2, 1, 1)

        self.label_6 = QLabel(TaskAdd)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 6, 1, 1, 1)

        self.label_4 = QLabel(TaskAdd)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)

        self.has_recurrence = QCheckBox(TaskAdd)
        self.has_recurrence.setObjectName(u"has_recurrence")

        self.gridLayout.addWidget(self.has_recurrence, 2, 3, 1, 1)

        self.label_5 = QLabel(TaskAdd)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 1, 1, 1)

        self.parent_task = QComboBox(TaskAdd)
        self.parent_task.setObjectName(u"parent_task")
        self.parent_task.setEnabled(False)
        self.parent_task.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)

        self.gridLayout.addWidget(self.parent_task, 6, 2, 1, 1)

        self.scheduled = QDateEdit(TaskAdd)
        self.scheduled.setObjectName(u"scheduled")
        self.scheduled.setEnabled(False)

        self.gridLayout.addWidget(self.scheduled, 3, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 7, 1, 1, 3)


        self.retranslateUi(TaskAdd)
        self.buttonBox.accepted.connect(TaskAdd.accept)
        self.buttonBox.rejected.connect(TaskAdd.reject)

        QMetaObject.connectSlotsByName(TaskAdd)
    # setupUi

    def retranslateUi(self, TaskAdd):
        TaskAdd.setWindowTitle(QCoreApplication.translate("TaskAdd", u"Add task", None))
        self.has_prioirty.setText(QCoreApplication.translate("TaskAdd", u"Has priority", None))
        self.deadline.setDisplayFormat(QCoreApplication.translate("TaskAdd", u"yyyy-MM-dd", None))
        self.label_3.setText(QCoreApplication.translate("TaskAdd", u"Recurrence:", None))
        self.has_deadline.setText(QCoreApplication.translate("TaskAdd", u"Has deadline", None))
        self.has_scheduled.setText(QCoreApplication.translate("TaskAdd", u"Has scheduled", None))
        self.has_parent_task.setText(QCoreApplication.translate("TaskAdd", u"Has parent task", None))
        self.label.setText(QCoreApplication.translate("TaskAdd", u"Description:", None))
        self.label_2.setText(QCoreApplication.translate("TaskAdd", u"Priority:", None))
        self.label_6.setText(QCoreApplication.translate("TaskAdd", u"Parent task:", None))
        self.label_4.setText(QCoreApplication.translate("TaskAdd", u"Scheduled:", None))
        self.has_recurrence.setText(QCoreApplication.translate("TaskAdd", u"Has recurrence", None))
        self.label_5.setText(QCoreApplication.translate("TaskAdd", u"Deadline:", None))
        self.scheduled.setDisplayFormat(QCoreApplication.translate("TaskAdd", u"yyyy-MM-dd", None))
    # retranslateUi

