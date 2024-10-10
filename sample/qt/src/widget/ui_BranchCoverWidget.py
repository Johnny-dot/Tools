# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BranchCoverWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_BranchCoverWidget(object):
    def setupUi(self, BranchCoverWidget):
        if not BranchCoverWidget.objectName():
            BranchCoverWidget.setObjectName(u"BranchCoverWidget")
        BranchCoverWidget.resize(911, 440)
        self.groupBox_2 = QGroupBox(BranchCoverWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(30, 40, 341, 61))
        font = QFont()
        font.setPointSize(12)
        self.groupBox_2.setFont(font)
        self.comboBox_main = QComboBox(self.groupBox_2)
        self.comboBox_main.setObjectName(u"comboBox_main")
        self.comboBox_main.setGeometry(QRect(10, 20, 321, 30))
        self.pushButton_build = QPushButton(BranchCoverWidget)
        self.pushButton_build.setObjectName(u"pushButton_build")
        self.pushButton_build.setGeometry(QRect(750, 50, 100, 50))
        self.pushButton_build.setFont(font)
        self.pushButton_build.setStyleSheet(u"QPushButton {\n"
"    background-color: #B0B0B0;  /* \u6d45\u7070\u8272 */\n"
"    color: white;               /* \u767d\u8272\u6587\u672c */\n"
"    border-radius: 10px;        /* \u5706\u89d2\u8fb9\u6846 */\n"
"    padding: 5px 15px;          /* \u5185\u8fb9\u8ddd */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #A0A0A0;  /* \u9f20\u6807\u60ac\u505c\u65f6\u7684\u989c\u8272 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #909090;  /* \u6309\u4e0b\u65f6\u7684\u989c\u8272 */\n"
"}\n"
"")
        self.groupBox_3 = QGroupBox(BranchCoverWidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(390, 40, 341, 61))
        self.groupBox_3.setFont(font)
        self.comboBox_ob = QComboBox(self.groupBox_3)
        self.comboBox_ob.setObjectName(u"comboBox_ob")
        self.comboBox_ob.setGeometry(QRect(10, 20, 321, 30))
        self.groupBox_4 = QGroupBox(BranchCoverWidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(30, 120, 821, 301))
        self.groupBox_4.setFont(font)
        self.textEdit_log = QTextEdit(self.groupBox_4)
        self.textEdit_log.setObjectName(u"textEdit_log")
        self.textEdit_log.setGeometry(QRect(10, 30, 791, 261))

        self.retranslateUi(BranchCoverWidget)

        QMetaObject.connectSlotsByName(BranchCoverWidget)
    # setupUi

    def retranslateUi(self, BranchCoverWidget):
        BranchCoverWidget.setWindowTitle(QCoreApplication.translate("BranchCoverWidget", u"Form", None))
#if QT_CONFIG(tooltip)
        self.groupBox_2.setToolTip(QCoreApplication.translate("BranchCoverWidget", u"\u9009\u62e9\u7528\u4e8e\u5408\u5e76\u7684\u4e3b\u7ebf\u5206\u652f\u4ee3\u7801", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.groupBox_2.setStatusTip(QCoreApplication.translate("BranchCoverWidget", u"\u9009\u62e9\u7528\u4e8e\u5408\u5e76\u7684\u4e3b\u7ebf\u5206\u652f\u4ee3\u7801", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.groupBox_2.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.groupBox_2.setTitle(QCoreApplication.translate("BranchCoverWidget", u"\u6e90\u5730\u5740", None))
        self.pushButton_build.setText(QCoreApplication.translate("BranchCoverWidget", u"\u540c\u6b65", None))
#if QT_CONFIG(tooltip)
        self.groupBox_3.setToolTip(QCoreApplication.translate("BranchCoverWidget", u"\u9009\u62e9\u5c06\u5408\u5e76\u7ed3\u679c\u63d0\u4ea4\u5230\u5177\u4f53\u7684\u5206\u652f", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.groupBox_3.setStatusTip(QCoreApplication.translate("BranchCoverWidget", u"\u9009\u62e9\u5c06\u5408\u5e76\u7ed3\u679c\u63d0\u4ea4\u5230\u5177\u4f53\u7684\u5206\u652f", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.groupBox_3.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.groupBox_3.setTitle(QCoreApplication.translate("BranchCoverWidget", u"\u76ee\u6807\u5730\u5740", None))
#if QT_CONFIG(tooltip)
        self.groupBox_4.setToolTip(QCoreApplication.translate("BranchCoverWidget", u"\u5728\u6b64\u8f93\u5165\u63d0\u4ea4\u5408\u5e76\u7ed3\u679c\u65f6\u7684\u65e5\u5fd7", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.groupBox_4.setStatusTip(QCoreApplication.translate("BranchCoverWidget", u"\u5728\u6b64\u8f93\u5165\u63d0\u4ea4\u5408\u5e76\u7ed3\u679c\u65f6\u7684\u65e5\u5fd7", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.groupBox_4.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.groupBox_4.setTitle(QCoreApplication.translate("BranchCoverWidget", u"\u63d0\u4ea4\u65e5\u5fd7", None))
        self.textEdit_log.setPlaceholderText(QCoreApplication.translate("BranchCoverWidget", u"\u5728\u6b64\u8f93\u5165\u63d0\u4ea4\u5408\u5e76\u7ed3\u679c\u65f6\u7684\u65e5\u5fd7", None))
    # retranslateUi

