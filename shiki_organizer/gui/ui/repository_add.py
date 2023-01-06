# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'repository_add.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_RepositoryAdd(object):
    def setupUi(self, RepositoryAdd):
        if not RepositoryAdd.objectName():
            RepositoryAdd.setObjectName(u"RepositoryAdd")
        RepositoryAdd.resize(468, 128)
        self.gridLayout = QGridLayout(RepositoryAdd)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(RepositoryAdd)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 4)

        self.name = QLineEdit(RepositoryAdd)
        self.name.setObjectName(u"name")

        self.gridLayout.addWidget(self.name, 0, 3, 1, 1)

        self.task = QComboBox(RepositoryAdd)
        self.task.setObjectName(u"task")
        self.task.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)

        self.gridLayout.addWidget(self.task, 1, 3, 1, 1)

        self.label = QLabel(RepositoryAdd)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)

        self.verticalSpacer = QSpacerItem(453, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 0, 1, 4)

        self.label_2 = QLabel(RepositoryAdd)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 3)


        self.retranslateUi(RepositoryAdd)
        self.buttonBox.accepted.connect(RepositoryAdd.accept)
        self.buttonBox.rejected.connect(RepositoryAdd.reject)

        QMetaObject.connectSlotsByName(RepositoryAdd)
    # setupUi

    def retranslateUi(self, RepositoryAdd):
        RepositoryAdd.setWindowTitle(QCoreApplication.translate("RepositoryAdd", u"Add repository", None))
        self.label.setText(QCoreApplication.translate("RepositoryAdd", u"Repository name (owner/repository):", None))
        self.label_2.setText(QCoreApplication.translate("RepositoryAdd", u"Root task:", None))
    # retranslateUi

