# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ResConvertWidget.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGroupBox,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QToolButton, QWidget)

from sample.qt.src.pyui.DragListWidget import DragListWidget

class Ui_ResConvertWidget(object):
    def setupUi(self, ResConvertWidget):
        if not ResConvertWidget.objectName():
            ResConvertWidget.setObjectName(u"ResConvertWidget")
        ResConvertWidget.resize(911, 440)
        self.pushButton_build = QPushButton(ResConvertWidget)
        self.pushButton_build.setObjectName(u"pushButton_build")
        self.pushButton_build.setGeometry(QRect(800, 20, 91, 31))
        self.label_allBranchesTip = QLabel(ResConvertWidget)
        self.label_allBranchesTip.setObjectName(u"label_allBranchesTip")
        self.label_allBranchesTip.setGeometry(QRect(20, 30, 53, 21))
        self.label_allBranchesTip.setStyleSheet(u"font: 10pt \"\u601d\u6e90\u9ed1\u4f53 CN Regular\";")
        self.comboBox_resPlatform = QComboBox(ResConvertWidget)
        self.comboBox_resPlatform.setObjectName(u"comboBox_resPlatform")
        self.comboBox_resPlatform.setGeometry(QRect(80, 30, 69, 22))
        self.groupBox = QGroupBox(ResConvertWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 70, 890, 361))
        self.listWidget_processed = QListWidget(self.groupBox)
        self.listWidget_processed.setObjectName(u"listWidget_processed")
        self.listWidget_processed.setGeometry(QRect(460, 20, 400, 331))
        self.listWidget_pending = DragListWidget(self.groupBox)
        self.listWidget_pending.setObjectName(u"listWidget_pending")
        self.listWidget_pending.setGeometry(QRect(30, 20, 400, 331))
        self.listWidget_pending.setAcceptDrops(True)
        self.listWidget_pending.setDragEnabled(True)
        self.listWidget_pending.setDragDropOverwriteMode(True)
        self.listWidget_pending.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(870, 100, 16, 141))
        self.label_3.setWordWrap(True)
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 100, 16, 141))
        self.label_2.setWordWrap(True)
        self.pushButton_emptyPending = QPushButton(self.groupBox)
        self.pushButton_emptyPending.setObjectName(u"pushButton_emptyPending")
        self.pushButton_emptyPending.setGeometry(QRect(400, 10, 40, 23))
        self.pushButton_emptyProcessed = QPushButton(self.groupBox)
        self.pushButton_emptyProcessed.setObjectName(u"pushButton_emptyProcessed")
        self.pushButton_emptyProcessed.setGeometry(QRect(830, 10, 40, 20))
        self.label_dropTips = QLabel(self.groupBox)
        self.label_dropTips.setObjectName(u"label_dropTips")
        self.label_dropTips.setGeometry(QRect(160, 160, 141, 41))
        self.label_dropTips.setMidLineWidth(0)
        self.label_dropTips.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.groupBox_2 = QGroupBox(ResConvertWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(170, 10, 190, 51))
        self.lineEdit_inPath = QLineEdit(self.groupBox_2)
        self.lineEdit_inPath.setObjectName(u"lineEdit_inPath")
        self.lineEdit_inPath.setGeometry(QRect(10, 20, 141, 21))
        self.toolButton_inPath = QToolButton(self.groupBox_2)
        self.toolButton_inPath.setObjectName(u"toolButton_inPath")
        self.toolButton_inPath.setGeometry(QRect(160, 20, 24, 21))
        self.groupBox_4 = QGroupBox(ResConvertWidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(380, 10, 190, 51))
        self.lineEdit_outPath = QLineEdit(self.groupBox_4)
        self.lineEdit_outPath.setObjectName(u"lineEdit_outPath")
        self.lineEdit_outPath.setGeometry(QRect(10, 20, 141, 21))
        self.toolButton_outPath = QToolButton(self.groupBox_4)
        self.toolButton_outPath.setObjectName(u"toolButton_outPath")
        self.toolButton_outPath.setGeometry(QRect(160, 20, 24, 21))
        self.groupBox_5 = QGroupBox(ResConvertWidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(590, 10, 190, 51))
        self.lineEdit_outPath_extra = QLineEdit(self.groupBox_5)
        self.lineEdit_outPath_extra.setObjectName(u"lineEdit_outPath_extra")
        self.lineEdit_outPath_extra.setGeometry(QRect(10, 20, 141, 21))
        self.toolButton_outPath_extra = QToolButton(self.groupBox_5)
        self.toolButton_outPath_extra.setObjectName(u"toolButton_outPath_extra")
        self.toolButton_outPath_extra.setGeometry(QRect(160, 20, 24, 21))

        self.retranslateUi(ResConvertWidget)

        QMetaObject.connectSlotsByName(ResConvertWidget)
    # setupUi

    def retranslateUi(self, ResConvertWidget):
        ResConvertWidget.setWindowTitle(QCoreApplication.translate("ResConvertWidget", u"Form", None))
        self.pushButton_build.setText(QCoreApplication.translate("ResConvertWidget", u"\u542f\u52a8", None))
        self.label_allBranchesTip.setText(QCoreApplication.translate("ResConvertWidget", u"\u64cd\u4f5c\u5e73\u53f0", None))
        self.groupBox.setTitle(QCoreApplication.translate("ResConvertWidget", u"\u663e\u793a\u533a", None))
        self.label_3.setText(QCoreApplication.translate("ResConvertWidget", u"\u5df2\u8f6c\u6587\u4ef6\u5217\u8868", None))
        self.label_2.setText(QCoreApplication.translate("ResConvertWidget", u"\u5f85\u8f6c\u6587\u4ef6\u5217\u8868", None))
        self.pushButton_emptyPending.setText(QCoreApplication.translate("ResConvertWidget", u"\u6e05\u7a7a", None))
        self.pushButton_emptyProcessed.setText(QCoreApplication.translate("ResConvertWidget", u"\u6e05\u7a7a", None))
        self.label_dropTips.setText(QCoreApplication.translate("ResConvertWidget", u"\u4ece\u7cfb\u7edf\u8d44\u6e90\u7ba1\u7406\u5668\u4e2d\n"
"\u62d6\u62fd\u8d44\u6e90\u81f3\u6b64", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ResConvertWidget", u"In", None))
        self.lineEdit_inPath.setPlaceholderText(QCoreApplication.translate("ResConvertWidget", u"\u8f93\u5165\u8def\u5f84", None))
        self.toolButton_inPath.setText(QCoreApplication.translate("ResConvertWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.groupBox_4.setToolTip(QCoreApplication.translate("ResConvertWidget", u"\u6307\u5b9a\u6587\u4ef6\u8f6c\u6362\u5b8c\u6210\u540e\u7684\u8f93\u51fa\u8def\u5f84", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.groupBox_4.setStatusTip(QCoreApplication.translate("ResConvertWidget", u"\u6307\u5b9a\u6587\u4ef6\u8f6c\u6362\u5b8c\u6210\u540e\u7684\u8f93\u51fa\u8def\u5f84", None))
#endif // QT_CONFIG(statustip)
        self.groupBox_4.setTitle(QCoreApplication.translate("ResConvertWidget", u"Out1", None))
        self.lineEdit_outPath.setText("")
        self.lineEdit_outPath.setPlaceholderText(QCoreApplication.translate("ResConvertWidget", u"\u8f93\u51fa\u8def\u5f84", None))
        self.toolButton_outPath.setText(QCoreApplication.translate("ResConvertWidget", u"...", None))
#if QT_CONFIG(tooltip)
        self.groupBox_5.setToolTip(QCoreApplication.translate("ResConvertWidget", u"\u76f8\u540c\u7684\u5185\u5bb9\u53ef\u4ee5\u9009\u5b9a\u989d\u5916\u8def\u5f84\u518d\u8f93\u51fa\u4e00\u6b21", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.groupBox_5.setStatusTip(QCoreApplication.translate("ResConvertWidget", u"\u76f8\u540c\u7684\u5185\u5bb9\u53ef\u4ee5\u9009\u5b9a\u989d\u5916\u8def\u5f84\u518d\u8f93\u51fa\u4e00\u6b21", None))
#endif // QT_CONFIG(statustip)
        self.groupBox_5.setTitle(QCoreApplication.translate("ResConvertWidget", u"Out2", None))
        self.lineEdit_outPath_extra.setText("")
        self.lineEdit_outPath_extra.setPlaceholderText(QCoreApplication.translate("ResConvertWidget", u"\u8f93\u51fa\u8def\u5f84", None))
        self.toolButton_outPath_extra.setText(QCoreApplication.translate("ResConvertWidget", u"...", None))
    # retranslateUi

