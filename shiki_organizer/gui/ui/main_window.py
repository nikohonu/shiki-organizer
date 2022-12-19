# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(708, 480)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.view = QTableView(self.centralwidget)
        self.view.setObjectName(u"view")
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout.addWidget(self.view)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_2.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_2.addWidget(self.pushButton_5)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_start = QPushButton(self.centralwidget)
        self.button_start.setObjectName(u"button_start")

        self.horizontalLayout.addWidget(self.button_start)

        self.button_stop = QPushButton(self.centralwidget)
        self.button_stop.setObjectName(u"button_stop")

        self.horizontalLayout.addWidget(self.button_stop)

        self.button_done = QPushButton(self.centralwidget)
        self.button_done.setObjectName(u"button_done")

        self.horizontalLayout.addWidget(self.button_done)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Shiki Organizer", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Add (A)", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Delete (D)", None))
        self.button_start.setText(QCoreApplication.translate("MainWindow", u"Start (S)", None))
        self.button_stop.setText(QCoreApplication.translate("MainWindow", u"Stop (Q)", None))
        self.button_done.setText(QCoreApplication.translate("MainWindow", u"Complete (C)", None))
    # retranslateUi

