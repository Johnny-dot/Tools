# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GMSerializeWidget.ui'
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
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QWidget)

from sample.qt.src.pyui.DragListWidget import DragListWidget

class Ui_GMSerializeWidget(object):
    def setupUi(self, GMSerializeWidget):
        if not GMSerializeWidget.objectName():
            GMSerializeWidget.setObjectName(u"GMSerializeWidget")
        GMSerializeWidget.resize(911, 440)
        self.pushButton_build = QPushButton(GMSerializeWidget)
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
        self.groupBox = QGroupBox(GMSerializeWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 70, 890, 361))
        self.groupBox.setFont(font)
        self.listWidget_processed = QListWidget(self.groupBox)
        self.listWidget_processed.setObjectName(u"listWidget_processed")
        self.listWidget_processed.setGeometry(QRect(459, 40, 401, 311))
        self.listWidget_pending = DragListWidget(self.groupBox)
        self.listWidget_pending.setObjectName(u"listWidget_pending")
        self.listWidget_pending.setGeometry(QRect(9, 40, 431, 311))
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
        self.label_4.setGeometry(QRect(460, 20, 151, 20))
        self.label_4.setFont(font1)
        self.label_4.setWordWrap(True)
        self.label_dropTips = QLabel(self.groupBox)
        self.label_dropTips.setObjectName(u"label_dropTips")
        self.label_dropTips.setGeometry(QRect(160, 170, 141, 41))
        self.label_dropTips.setMidLineWidth(0)
        self.label_dropTips.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.retranslateUi(GMSerializeWidget)

        QMetaObject.connectSlotsByName(GMSerializeWidget)
    # setupUi

    def retranslateUi(self, GMSerializeWidget):
        GMSerializeWidget.setWindowTitle(QCoreApplication.translate("GMSerializeWidget", u"Form", None))
        self.pushButton_build.setText(QCoreApplication.translate("GMSerializeWidget", u"\u5e8f\u5217\u5316", None))
        self.groupBox.setTitle(QCoreApplication.translate("GMSerializeWidget", u"\u663e\u793a\u533a", None))
        self.label_2.setText(QCoreApplication.translate("GMSerializeWidget", u"\u5f85\u5e8f\u5217\u5316\u7684\u5185\u5bb9", None))
        self.label_4.setText(QCoreApplication.translate("GMSerializeWidget", u"\u5df2\u5b8c\u6210\u5e8f\u5217\u5316\u7684\u5185\u5bb9", None))
        self.label_dropTips.setText(QCoreApplication.translate("GMSerializeWidget", u"\u4ece\u7cfb\u7edf\u8d44\u6e90\u7ba1\u7406\u5668\u4e2d\n"
"\u62d6\u62fd\u8d44\u6e90\u81f3\u6b64", None))
    # retranslateUi

