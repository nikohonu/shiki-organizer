# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interval_add.ui'
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
    QDateEdit, QDateTimeEdit, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QSizePolicy, QSpacerItem,
    QTimeEdit, QWidget)

class Ui_IntervalAdd(object):
    def setupUi(self, IntervalAdd):
        if not IntervalAdd.objectName():
            IntervalAdd.setObjectName(u"IntervalAdd")
        IntervalAdd.resize(506, 176)
        self.gridLayout = QGridLayout(IntervalAdd)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(IntervalAdd)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 5, 3, 1, 1)

        self.start = QTimeEdit(IntervalAdd)
        self.start.setObjectName(u"start")
        self.start.setTimeSpec(Qt.LocalTime)

        self.gridLayout.addWidget(self.start, 6, 1, 1, 1)

        self.label_5 = QLabel(IntervalAdd)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 5, 2, 1, 1)

        self.label_4 = QLabel(IntervalAdd)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 5, 1, 1, 1)

        self.has_end = QCheckBox(IntervalAdd)
        self.has_end.setObjectName(u"has_end")
        self.has_end.setChecked(True)

        self.gridLayout.addWidget(self.has_end, 6, 6, 1, 1)

        self.end = QTimeEdit(IntervalAdd)
        self.end.setObjectName(u"end")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.end.sizePolicy().hasHeightForWidth())
        self.end.setSizePolicy(sizePolicy)
        self.end.setTimeSpec(Qt.LocalTime)

        self.gridLayout.addWidget(self.end, 6, 2, 1, 1)

        self.date = QDateEdit(IntervalAdd)
        self.date.setObjectName(u"date")
        self.date.setTimeSpec(Qt.LocalTime)

        self.gridLayout.addWidget(self.date, 6, 0, 1, 1)

        self.label_3 = QLabel(IntervalAdd)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)

        self.duration = QTimeEdit(IntervalAdd)
        self.duration.setObjectName(u"duration")
        self.duration.setCurrentSection(QDateTimeEdit.MinuteSection)
        self.duration.setTimeSpec(Qt.LocalTime)

        self.gridLayout.addWidget(self.duration, 6, 3, 1, 1)

        self.task = QComboBox(IntervalAdd)
        self.task.setObjectName(u"task")
        self.task.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.task.setDuplicatesEnabled(False)
        self.task.setFrame(True)

        self.gridLayout.addWidget(self.task, 1, 0, 1, 7)

        self.label = QLabel(IntervalAdd)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.buttonBox = QDialogButtonBox(IntervalAdd)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 7)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 7, 0, 1, 7)


        self.retranslateUi(IntervalAdd)
        self.buttonBox.accepted.connect(IntervalAdd.accept)
        self.buttonBox.rejected.connect(IntervalAdd.reject)

        QMetaObject.connectSlotsByName(IntervalAdd)
    # setupUi

    def retranslateUi(self, IntervalAdd):
        IntervalAdd.setWindowTitle(QCoreApplication.translate("IntervalAdd", u"Add interval", None))
        self.label_2.setText(QCoreApplication.translate("IntervalAdd", u"Duration", None))
        self.start.setDisplayFormat(QCoreApplication.translate("IntervalAdd", u"HH:mm:ss", None))
        self.label_5.setText(QCoreApplication.translate("IntervalAdd", u"End", None))
        self.label_4.setText(QCoreApplication.translate("IntervalAdd", u"Start", None))
        self.has_end.setText(QCoreApplication.translate("IntervalAdd", u"Has an end?", None))
        self.end.setDisplayFormat(QCoreApplication.translate("IntervalAdd", u"HH:mm:ss", None))
        self.date.setDisplayFormat(QCoreApplication.translate("IntervalAdd", u"yyyy-MM-dd", None))
        self.label_3.setText(QCoreApplication.translate("IntervalAdd", u"Date", None))
        self.duration.setDisplayFormat(QCoreApplication.translate("IntervalAdd", u"HH:mm:ss", None))
        self.label.setText(QCoreApplication.translate("IntervalAdd", u"Task", None))
    # retranslateUi

