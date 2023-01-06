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
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QTabWidget,
    QToolBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.action_task_add = QAction(MainWindow)
        self.action_task_add.setObjectName(u"action_task_add")
        self.action_interval_start = QAction(MainWindow)
        self.action_interval_start.setObjectName(u"action_interval_start")
        self.action_interval_stop = QAction(MainWindow)
        self.action_interval_stop.setObjectName(u"action_interval_stop")
        self.action_task_complete = QAction(MainWindow)
        self.action_task_complete.setObjectName(u"action_task_complete")
        self.action_delete = QAction(MainWindow)
        self.action_delete.setObjectName(u"action_delete")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tab_widget = QTabWidget(self.centralwidget)
        self.tab_widget.setObjectName(u"tab_widget")

        self.gridLayout.addWidget(self.tab_widget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 26))
        self.menuTask = QMenu(self.menubar)
        self.menuTask.setObjectName(u"menuTask")
        self.menuIntervals = QMenu(self.menubar)
        self.menuIntervals.setObjectName(u"menuIntervals")
        self.menuAction = QMenu(self.menubar)
        self.menuAction.setObjectName(u"menuAction")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuAction.menuAction())
        self.menubar.addAction(self.menuTask.menuAction())
        self.menubar.addAction(self.menuIntervals.menuAction())
        self.menuTask.addAction(self.action_task_add)
        self.menuTask.addAction(self.action_task_complete)
        self.menuIntervals.addAction(self.action_interval_start)
        self.menuIntervals.addAction(self.action_interval_stop)
        self.menuAction.addAction(self.action_delete)
        self.toolBar.addAction(self.action_task_add)
        self.toolBar.addAction(self.action_task_complete)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_interval_start)
        self.toolBar.addAction(self.action_interval_stop)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_delete)

        self.retranslateUi(MainWindow)

        self.tab_widget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Shiki Organizer", None))
        self.action_task_add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
#if QT_CONFIG(shortcut)
        self.action_task_add.setShortcut(QCoreApplication.translate("MainWindow", u"A", None))
#endif // QT_CONFIG(shortcut)
        self.action_interval_start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
#if QT_CONFIG(shortcut)
        self.action_interval_start.setShortcut(QCoreApplication.translate("MainWindow", u"S", None))
#endif // QT_CONFIG(shortcut)
        self.action_interval_stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
#if QT_CONFIG(shortcut)
        self.action_interval_stop.setShortcut(QCoreApplication.translate("MainWindow", u"P", None))
#endif // QT_CONFIG(shortcut)
        self.action_task_complete.setText(QCoreApplication.translate("MainWindow", u"Complete", None))
#if QT_CONFIG(shortcut)
        self.action_task_complete.setShortcut(QCoreApplication.translate("MainWindow", u"C", None))
#endif // QT_CONFIG(shortcut)
        self.action_delete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
#if QT_CONFIG(shortcut)
        self.action_delete.setShortcut(QCoreApplication.translate("MainWindow", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.menuTask.setTitle(QCoreApplication.translate("MainWindow", u"Task", None))
        self.menuIntervals.setTitle(QCoreApplication.translate("MainWindow", u"Interval", None))
        self.menuAction.setTitle(QCoreApplication.translate("MainWindow", u"Action", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

