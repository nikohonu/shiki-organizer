# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_tab.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_SettingsTab(object):
    def setupUi(self, SettingsTab):
        if not SettingsTab.objectName():
            SettingsTab.setObjectName(u"SettingsTab")
        SettingsTab.resize(823, 594)
        self.verticalLayout = QVBoxLayout(SettingsTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(SettingsTab)
        self.label.setObjectName(u"label")
        self.label.setOpenExternalLinks(True)

        self.horizontalLayout.addWidget(self.label)

        self.github_token = QLineEdit(SettingsTab)
        self.github_token.setObjectName(u"github_token")

        self.horizontalLayout.addWidget(self.github_token)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(SettingsTab)

        QMetaObject.connectSlotsByName(SettingsTab)
    # setupUi

    def retranslateUi(self, SettingsTab):
        SettingsTab.setWindowTitle(QCoreApplication.translate("SettingsTab", u"Form", None))
        self.label.setText(QCoreApplication.translate("SettingsTab", u"GitHub personal access tokens:", None))
    # retranslateUi

