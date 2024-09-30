# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DetectDuplicateFilesWidget.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGroupBox, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QToolButton, QWidget)

class Ui_DetectDuplicateFilesWidget(object):
    def setupUi(self, DetectDuplicateFilesWidget):
        if not DetectDuplicateFilesWidget.objectName():
            DetectDuplicateFilesWidget.setObjectName(u"DetectDuplicateFilesWidget")
        DetectDuplicateFilesWidget.resize(911, 440)
        self.pushButton_build = QPushButton(DetectDuplicateFilesWidget)
        self.pushButton_build.setObjectName(u"pushButton_build")
        self.pushButton_build.setGeometry(QRect(780, 20, 100, 50))
        font = QFont()
        font.setPointSize(12)
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
        self.groupBox = QGroupBox(DetectDuplicateFilesWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 70, 890, 361))
        self.groupBox.setFont(font)
        self.listWidget_processed = QListWidget(self.groupBox)
        self.listWidget_processed.setObjectName(u"listWidget_processed")
        self.listWidget_processed.setGeometry(QRect(359, 40, 501, 311))
        self.listWidget_pending = QListWidget(self.groupBox)
        self.listWidget_pending.setObjectName(u"listWidget_pending")
        self.listWidget_pending.setGeometry(QRect(9, 40, 321, 311))
        self.listWidget_pending.setAcceptDrops(True)
        self.listWidget_pending.setDragEnabled(True)
        self.listWidget_pending.setDragDropOverwriteMode(True)
        self.listWidget_pending.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 20, 241, 20))
        font1 = QFont()
        font1.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font1.setPointSize(11)
        self.label_2.setFont(font1)
        self.label_2.setWordWrap(True)
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(360, 20, 151, 20))
        self.label_4.setFont(font1)
        self.label_4.setWordWrap(True)
        self.groupBox_2 = QGroupBox(DetectDuplicateFilesWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 10, 331, 51))
        self.groupBox_2.setFont(font)
        self.lineEdit_inPath = QLineEdit(self.groupBox_2)
        self.lineEdit_inPath.setObjectName(u"lineEdit_inPath")
        self.lineEdit_inPath.setGeometry(QRect(10, 20, 281, 21))
        self.toolButton_inPath = QToolButton(self.groupBox_2)
        self.toolButton_inPath.setObjectName(u"toolButton_inPath")
        self.toolButton_inPath.setGeometry(QRect(300, 20, 24, 21))
        self.groupBox_3 = QGroupBox(DetectDuplicateFilesWidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(370, 10, 391, 51))
        self.lineEdit_match = QLineEdit(self.groupBox_3)
        self.lineEdit_match.setObjectName(u"lineEdit_match")
        self.lineEdit_match.setGeometry(QRect(10, 20, 361, 21))

        self.retranslateUi(DetectDuplicateFilesWidget)

        QMetaObject.connectSlotsByName(DetectDuplicateFilesWidget)
    # setupUi

    def retranslateUi(self, DetectDuplicateFilesWidget):
        DetectDuplicateFilesWidget.setWindowTitle(QCoreApplication.translate("DetectDuplicateFilesWidget", u"Form", None))
        self.pushButton_build.setText(QCoreApplication.translate("DetectDuplicateFilesWidget", u"\u542f\u52a8", None))
        self.groupBox.setTitle(QCoreApplication.translate("DetectDuplicateFilesWidget", u"\u663e\u793a\u533a", None))
        self.label_2.setText(QCoreApplication.translate("DetectDuplicateFilesWidget", u"\u5df2\u68c0\u51fa\u5b58\u5728\u91cd\u590d\u7684\u6587\u4ef6\u5217\u8868", None))
        self.label_4.setText(QCoreApplication.translate("DetectDuplicateFilesWidget", u"\u91cd\u590d\u5185\u5bb9\u8be6\u60c5", None))
#if QT_CONFIG(tooltip)
        self.groupBox_2.setToolTip(QCoreApplication.translate("DetectDuplicateFilesWidget", u"<html><head/><body><p>\u5728\u6b64\u8f93\u5165\u5f85\u68c0\u6d4b\u91cd\u590d\u5185\u5bb9\u7684\u6587\u4ef6\u8def\u5f84</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.groupBox_2.setStatusTip(QCoreApplication.translate("DetectDuplicateFilesWidget", u"<html><head/><body><p>\u5728\u6b64\u8f93\u5165\u5f85\u68c0\u6d4b\u91cd\u590d\u5185\u5bb9\u7684\u6587\u4ef6\u8def\u5f84</p></body></html>", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.groupBox_2.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.groupBox_2.setTitle(QCoreApplication.translate("DetectDuplicateFilesWidget", u"In", None))
        self.lineEdit_inPath.setPlaceholderText(QCoreApplication.translate("DetectDuplicateFilesWidget", u"\u8f93\u5165\u8def\u5f84", None))
        self.toolButton_inPath.setText(QCoreApplication.translate("DetectDuplicateFilesWidget", u"...", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("DetectDuplicateFilesWidget", u"\u901a\u914d\u7b26\u5339\u914d", None))
        self.lineEdit_match.setPlaceholderText(QCoreApplication.translate("DetectDuplicateFilesWidget", u"\u6307\u5b9a\u5339\u914d\u89c4\u5219\uff0c\u4f8b\u5982*.pfx ", None))
    # retranslateUi

