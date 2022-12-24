# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interval_tab.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTableView, QVBoxLayout, QWidget)

class Ui_IntervalTab(object):
    def setupUi(self, IntervalTab):
        if not IntervalTab.objectName():
            IntervalTab.setObjectName(u"IntervalTab")
        IntervalTab.resize(944, 591)
        self.verticalLayout = QVBoxLayout(IntervalTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(IntervalTab)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.period = QComboBox(IntervalTab)
        self.period.addItem("")
        self.period.addItem("")
        self.period.addItem("")
        self.period.addItem("")
        self.period.addItem("")
        self.period.setObjectName(u"period")

        self.horizontalLayout.addWidget(self.period)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.view = QTableView(IntervalTab)
        self.view.setObjectName(u"view")
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.view)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.status = QLabel(IntervalTab)
        self.status.setObjectName(u"status")

        self.horizontalLayout_2.addWidget(self.status)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.button_add = QPushButton(IntervalTab)
        self.button_add.setObjectName(u"button_add")

        self.horizontalLayout_2.addWidget(self.button_add)

        self.button_delete = QPushButton(IntervalTab)
        self.button_delete.setObjectName(u"button_delete")

        self.horizontalLayout_2.addWidget(self.button_delete)

        self.button_modify = QPushButton(IntervalTab)
        self.button_modify.setObjectName(u"button_modify")

        self.horizontalLayout_2.addWidget(self.button_modify)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(IntervalTab)

        QMetaObject.connectSlotsByName(IntervalTab)
    # setupUi

    def retranslateUi(self, IntervalTab):
        IntervalTab.setWindowTitle(QCoreApplication.translate("IntervalTab", u"Form", None))
        self.label.setText(QCoreApplication.translate("IntervalTab", u"Period:", None))
        self.period.setItemText(0, QCoreApplication.translate("IntervalTab", u"All", None))
        self.period.setItemText(1, QCoreApplication.translate("IntervalTab", u"Today", None))
        self.period.setItemText(2, QCoreApplication.translate("IntervalTab", u"Week", None))
        self.period.setItemText(3, QCoreApplication.translate("IntervalTab", u"Month", None))
        self.period.setItemText(4, QCoreApplication.translate("IntervalTab", u"Year", None))

        self.period.setCurrentText(QCoreApplication.translate("IntervalTab", u"All", None))
        self.status.setText(QCoreApplication.translate("IntervalTab", u"Total duration:", None))
        self.button_add.setText(QCoreApplication.translate("IntervalTab", u"Add", None))
        self.button_delete.setText(QCoreApplication.translate("IntervalTab", u"Delete", None))
        self.button_modify.setText(QCoreApplication.translate("IntervalTab", u"Modify", None))
    # retranslateUi

