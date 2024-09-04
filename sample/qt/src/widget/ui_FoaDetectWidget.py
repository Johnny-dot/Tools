# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FoaDetectWidget.ui'
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

from sample.qt.src.pyui.DragListWidget import DragListWidget

class Ui_FoaDetectWidget(object):
    def setupUi(self, FoaDetectWidget):
        if not FoaDetectWidget.objectName():
            FoaDetectWidget.setObjectName(u"FoaDetectWidget")
        FoaDetectWidget.resize(911, 440)
        self.pushButton_build = QPushButton(FoaDetectWidget)
        self.pushButton_build.setObjectName(u"pushButton_build")
        self.pushButton_build.setGeometry(QRect(770, 15, 100, 50))
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
        self.groupBox = QGroupBox(FoaDetectWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 70, 890, 361))
        self.groupBox.setFont(font)
        self.listWidget_processed = QListWidget(self.groupBox)
        self.listWidget_processed.setObjectName(u"listWidget_processed")
        self.listWidget_processed.setGeometry(QRect(269, 40, 591, 311))
        self.listWidget_pending = DragListWidget(self.groupBox)
        self.listWidget_pending.setObjectName(u"listWidget_pending")
        self.listWidget_pending.setGeometry(QRect(9, 40, 231, 311))
        self.listWidget_pending.setAcceptDrops(True)
        self.listWidget_pending.setDragEnabled(True)
        self.listWidget_pending.setDragDropOverwriteMode(True)
        self.listWidget_pending.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 20, 151, 20))
        font1 = QFont()
        font1.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font1.setPointSize(11)
        self.label_2.setFont(font1)
        self.label_2.setWordWrap(True)
        self.pushButton_emptyPending = QPushButton(self.groupBox)
        self.pushButton_emptyPending.setObjectName(u"pushButton_emptyPending")
        self.pushButton_emptyPending.setGeometry(QRect(190, 18, 51, 21))
        self.pushButton_emptyPending.setStyleSheet(u"    QPushButton {\n"
"        background-color: red;        /* \u80cc\u666f\u8272\u8bbe\u4e3a\u7ea2\u8272\uff0c\u8b66\u793a\u6548\u679c */\n"
"        color: white;                 /* \u6587\u5b57\u989c\u8272\u8bbe\u4e3a\u767d\u8272 */\n"
"        border: 2px solid #cc0000;    /* \u8fb9\u6846\u989c\u8272\u7a0d\u6df1\uff0c\u7a81\u51fa\u6309\u94ae */\n"
"        border-radius: 10px;          /* \u5706\u89d2\u8fb9\u6846 */\n"
"        padding: 1px;                 /* \u51cf\u5c11\u5185\u8fb9\u8ddd\uff0c\u4ee5\u4fbf\u663e\u793a\u5b8c\u6574\u6587\u672c */\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: #ff6666;    /* \u9f20\u6807\u60ac\u505c\u65f6\u80cc\u666f\u8272\u53d8\u6d45 */\n"
"        border: 2px solid #ff3333;    /* \u60ac\u505c\u65f6\u8fb9\u6846\u989c\u8272\u53d8\u6d45 */\n"
"    }\n"
"    QPushButton:pressed {\n"
"        background-color: #cc0000;    /* \u6309\u4e0b\u65f6\u80cc\u666f\u8272\u7a0d\u6df1 */\n"
"        border: 2px solid #990000;    /* \u6309\u4e0b\u65f6\u8fb9\u6846\u989c"
                        "\u8272\u66f4\u6df1 */\n"
"    }")
        self.label_dropTips = QLabel(self.groupBox)
        self.label_dropTips.setObjectName(u"label_dropTips")
        self.label_dropTips.setGeometry(QRect(60, 170, 141, 41))
        self.label_dropTips.setMidLineWidth(0)
        self.label_dropTips.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(270, 20, 151, 20))
        self.label_4.setFont(font1)
        self.label_4.setWordWrap(True)
        self.groupBox_2 = QGroupBox(FoaDetectWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 10, 481, 51))
        self.groupBox_2.setFont(font)
        self.lineEdit_inPath = QLineEdit(self.groupBox_2)
        self.lineEdit_inPath.setObjectName(u"lineEdit_inPath")
        self.lineEdit_inPath.setGeometry(QRect(10, 20, 431, 21))
        self.toolButton_inPath = QToolButton(self.groupBox_2)
        self.toolButton_inPath.setObjectName(u"toolButton_inPath")
        self.toolButton_inPath.setGeometry(QRect(450, 20, 24, 21))

        self.retranslateUi(FoaDetectWidget)

        QMetaObject.connectSlotsByName(FoaDetectWidget)
    # setupUi

    def retranslateUi(self, FoaDetectWidget):
        FoaDetectWidget.setWindowTitle(QCoreApplication.translate("FoaDetectWidget", u"Form", None))
        self.pushButton_build.setText(QCoreApplication.translate("FoaDetectWidget", u"\u542f\u52a8", None))
        self.groupBox.setTitle(QCoreApplication.translate("FoaDetectWidget", u"\u663e\u793a\u533a", None))
        self.label_2.setText(QCoreApplication.translate("FoaDetectWidget", u"FOA\u5f85\u68c0\u5217\u8868", None))
        self.pushButton_emptyPending.setText(QCoreApplication.translate("FoaDetectWidget", u"\u6e05\u7a7a", None))
        self.label_dropTips.setText(QCoreApplication.translate("FoaDetectWidget", u"\u4ece\u7cfb\u7edf\u8d44\u6e90\u7ba1\u7406\u5668\u4e2d\n"
"\u62d6\u62fd\u8d44\u6e90\u81f3\u6b64", None))
        self.label_4.setText(QCoreApplication.translate("FoaDetectWidget", u"\u4e0d\u5408\u89c4\u7684FOA\u6587\u4ef6\u5217\u8868", None))
#if QT_CONFIG(tooltip)
        self.groupBox_2.setToolTip(QCoreApplication.translate("FoaDetectWidget", u"<html><head/><body><p>\u5728\u6b64\u8f93\u5165\u5f85\u68c0\u6d4b\u91cd\u590d\u5185\u5bb9\u7684\u6587\u4ef6\u8def\u5f84</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.groupBox_2.setStatusTip(QCoreApplication.translate("FoaDetectWidget", u"<html><head/><body><p>\u5728\u6b64\u8f93\u5165\u5f85\u68c0\u6d4b\u91cd\u590d\u5185\u5bb9\u7684\u6587\u4ef6\u8def\u5f84</p></body></html>", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.groupBox_2.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.groupBox_2.setTitle(QCoreApplication.translate("FoaDetectWidget", u"In", None))
        self.lineEdit_inPath.setPlaceholderText(QCoreApplication.translate("FoaDetectWidget", u"\u8f93\u5165\u8def\u5f84", None))
        self.toolButton_inPath.setText(QCoreApplication.translate("FoaDetectWidget", u"...", None))
    # retranslateUi

