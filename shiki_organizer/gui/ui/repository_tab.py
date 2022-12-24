# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'repository_tab.ui'
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

class Ui_RepositoryTab(object):
    def setupUi(self, RepositoryTab):
        if not RepositoryTab.objectName():
            RepositoryTab.setObjectName(u"RepositoryTab")
        RepositoryTab.resize(906, 586)
        self.verticalLayout = QVBoxLayout(RepositoryTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.view = QTableView(RepositoryTab)
        self.view.setObjectName(u"view")
        self.view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.view.setSortingEnabled(True)
        self.view.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.view)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.button_add = QPushButton(RepositoryTab)
        self.button_add.setObjectName(u"button_add")

        self.horizontalLayout_2.addWidget(self.button_add)

        self.button_delete = QPushButton(RepositoryTab)
        self.button_delete.setObjectName(u"button_delete")

        self.horizontalLayout_2.addWidget(self.button_delete)

        self.button_modify = QPushButton(RepositoryTab)
        self.button_modify.setObjectName(u"button_modify")

        self.horizontalLayout_2.addWidget(self.button_modify)

        self.button_pull = QPushButton(RepositoryTab)
        self.button_pull.setObjectName(u"button_pull")

        self.horizontalLayout_2.addWidget(self.button_pull)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(RepositoryTab)

        QMetaObject.connectSlotsByName(RepositoryTab)
    # setupUi

    def retranslateUi(self, RepositoryTab):
        RepositoryTab.setWindowTitle(QCoreApplication.translate("RepositoryTab", u"Form", None))
        self.button_add.setText(QCoreApplication.translate("RepositoryTab", u"Add", None))
        self.button_delete.setText(QCoreApplication.translate("RepositoryTab", u"Delete", None))
        self.button_modify.setText(QCoreApplication.translate("RepositoryTab", u"Modify", None))
        self.button_pull.setText(QCoreApplication.translate("RepositoryTab", u"Pull", None))
    # retranslateUi

