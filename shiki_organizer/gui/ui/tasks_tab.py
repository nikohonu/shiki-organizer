# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tasks_tab.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QPushButton, QSizePolicy, QSpacerItem, QTableView,
    QVBoxLayout, QWidget)

class Ui_TaskTab(object):
    def setupUi(self, TaskTab):
        if not TaskTab.objectName():
            TaskTab.setObjectName(u"TaskTab")
        TaskTab.resize(619, 471)
        self.verticalLayout = QVBoxLayout(TaskTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.view = QTableView(TaskTab)
        self.view.setObjectName(u"view")
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.view)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button_add = QPushButton(TaskTab)
        self.button_add.setObjectName(u"button_add")

        self.horizontalLayout_2.addWidget(self.button_add)

        self.button_delete = QPushButton(TaskTab)
        self.button_delete.setObjectName(u"button_delete")

        self.horizontalLayout_2.addWidget(self.button_delete)

        self.button_modify = QPushButton(TaskTab)
        self.button_modify.setObjectName(u"button_modify")

        self.horizontalLayout_2.addWidget(self.button_modify)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_start = QPushButton(TaskTab)
        self.button_start.setObjectName(u"button_start")

        self.horizontalLayout.addWidget(self.button_start)

        self.button_stop = QPushButton(TaskTab)
        self.button_stop.setObjectName(u"button_stop")

        self.horizontalLayout.addWidget(self.button_stop)

        self.button_done = QPushButton(TaskTab)
        self.button_done.setObjectName(u"button_done")

        self.horizontalLayout.addWidget(self.button_done)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(TaskTab)

        QMetaObject.connectSlotsByName(TaskTab)
    # setupUi

    def retranslateUi(self, TaskTab):
        TaskTab.setWindowTitle(QCoreApplication.translate("TaskTab", u"Form", None))
        self.button_add.setText(QCoreApplication.translate("TaskTab", u"Add (A)", None))
        self.button_delete.setText(QCoreApplication.translate("TaskTab", u"Delete (D)", None))
        self.button_modify.setText(QCoreApplication.translate("TaskTab", u"Modify (E)", None))
        self.button_start.setText(QCoreApplication.translate("TaskTab", u"Start (S)", None))
        self.button_stop.setText(QCoreApplication.translate("TaskTab", u"Stop (Q)", None))
        self.button_done.setText(QCoreApplication.translate("TaskTab", u"Complete (C)", None))
    # retranslateUi

