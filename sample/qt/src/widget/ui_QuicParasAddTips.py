# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'QuicParasAddTips.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QLineEdit, QSizePolicy, QWidget)

class Ui_QuicParasAddTipsDialog(object):
    def setupUi(self, QuicParasAddTipsDialog):
        if not QuicParasAddTipsDialog.objectName():
            QuicParasAddTipsDialog.setObjectName(u"QuicParasAddTipsDialog")
        QuicParasAddTipsDialog.resize(240, 171)
        self.buttonBox = QDialogButtonBox(QuicParasAddTipsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(-140, 120, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.label = QLabel(QuicParasAddTipsDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 30, 181, 21))
        self.label.setStyleSheet(u"")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit_input = QLineEdit(QuicParasAddTipsDialog)
        self.lineEdit_input.setObjectName(u"lineEdit_input")
        self.lineEdit_input.setGeometry(QRect(30, 70, 181, 21))

        self.retranslateUi(QuicParasAddTipsDialog)
        self.buttonBox.accepted.connect(QuicParasAddTipsDialog.accept)
        self.buttonBox.rejected.connect(QuicParasAddTipsDialog.reject)

        QMetaObject.connectSlotsByName(QuicParasAddTipsDialog)
    # setupUi

    def retranslateUi(self, QuicParasAddTipsDialog):
        QuicParasAddTipsDialog.setWindowTitle(QCoreApplication.translate("QuicParasAddTipsDialog", u"QuicParasAddTips", None))
        self.label.setText(QCoreApplication.translate("QuicParasAddTipsDialog", u"\u8bf7\u8f93\u5165\u5feb\u901f\u53c2\u6570\u7684\u540d\u79f0", None))
    # retranslateUi

