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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QSizePolicy,
    QTableView, QWidget)

class Ui_TaskTab(object):
    def setupUi(self, TaskTab):
        if not TaskTab.objectName():
            TaskTab.setObjectName(u"TaskTab")
        TaskTab.resize(602, 406)
        self.gridLayout = QGridLayout(TaskTab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.view = QTableView(TaskTab)
        self.view.setObjectName(u"view")

        self.gridLayout.addWidget(self.view, 0, 0, 1, 1)


        self.retranslateUi(TaskTab)

        QMetaObject.connectSlotsByName(TaskTab)
    # setupUi

    def retranslateUi(self, TaskTab):
        TaskTab.setWindowTitle(QCoreApplication.translate("TaskTab", u"Form", None))
    # retranslateUi

