# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interval_modify.ui'
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
    QDateTimeEdit, QDialog, QDialogButtonBox, QGridLayout,
    QLabel, QSizePolicy, QSpacerItem, QWidget)

class Ui_IntervalModify(object):
    def setupUi(self, IntervalModify):
        if not IntervalModify.objectName():
            IntervalModify.setObjectName(u"IntervalModify")
        IntervalModify.resize(312, 307)
        self.gridLayout = QGridLayout(IntervalModify)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(IntervalModify)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.task = QComboBox(IntervalModify)
        self.task.setObjectName(u"task")

        self.gridLayout.addWidget(self.task, 1, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(IntervalModify)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 11, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 10, 0, 1, 1)

        self.label_3 = QLabel(IntervalModify)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.start = QDateTimeEdit(IntervalModify)
        self.start.setObjectName(u"start")

        self.gridLayout.addWidget(self.start, 3, 0, 1, 1)

        self.label = QLabel(IntervalModify)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.end = QDateTimeEdit(IntervalModify)
        self.end.setObjectName(u"end")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.end.sizePolicy().hasHeightForWidth())
        self.end.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.end, 6, 0, 1, 1)

        self.end_none = QCheckBox(IntervalModify)
        self.end_none.setObjectName(u"end_none")

        self.gridLayout.addWidget(self.end_none, 6, 1, 1, 1)


        self.retranslateUi(IntervalModify)
        self.buttonBox.accepted.connect(IntervalModify.accept)
        self.buttonBox.rejected.connect(IntervalModify.reject)

        QMetaObject.connectSlotsByName(IntervalModify)
    # setupUi

    def retranslateUi(self, IntervalModify):
        IntervalModify.setWindowTitle(QCoreApplication.translate("IntervalModify", u"Modify interval", None))
        self.label_2.setText(QCoreApplication.translate("IntervalModify", u"Start", None))
        self.label_3.setText(QCoreApplication.translate("IntervalModify", u"End", None))
        self.start.setDisplayFormat(QCoreApplication.translate("IntervalModify", u"yyyy-MM-dd HH:mm:ss", None))
        self.label.setText(QCoreApplication.translate("IntervalModify", u"Task", None))
        self.end.setDisplayFormat(QCoreApplication.translate("IntervalModify", u"yyyy-MM-dd HH:mm:ss", None))
        self.end_none.setText(QCoreApplication.translate("IntervalModify", u"None", None))
    # retranslateUi

