# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FilesMD5Snapshot.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHeaderView, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QToolButton, QWidget)

class Ui_FilesMD5Snapshot(object):
    def setupUi(self, FilesMD5Snapshot):
        if not FilesMD5Snapshot.objectName():
            FilesMD5Snapshot.setObjectName(u"FilesMD5Snapshot")
        FilesMD5Snapshot.resize(911, 440)
        self.lineEdit_targetPath = QLineEdit(FilesMD5Snapshot)
        self.lineEdit_targetPath.setObjectName(u"lineEdit_targetPath")
        self.lineEdit_targetPath.setGeometry(QRect(90, 10, 311, 21))
        self.pushButton_export = QPushButton(FilesMD5Snapshot)
        self.pushButton_export.setObjectName(u"pushButton_export")
        self.pushButton_export.setGeometry(QRect(720, 40, 75, 23))
        self.label_buildTip_4 = QLabel(FilesMD5Snapshot)
        self.label_buildTip_4.setObjectName(u"label_buildTip_4")
        self.label_buildTip_4.setGeometry(QRect(22, 10, 61, 21))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(11)
        self.label_buildTip_4.setFont(font)
        self.label_buildTip_4.setStyleSheet(u"")
        self.toolButton_targetPath = QToolButton(FilesMD5Snapshot)
        self.toolButton_targetPath.setObjectName(u"toolButton_targetPath")
        self.toolButton_targetPath.setGeometry(QRect(410, 10, 24, 21))
        self.label_buildTip_5 = QLabel(FilesMD5Snapshot)
        self.label_buildTip_5.setObjectName(u"label_buildTip_5")
        self.label_buildTip_5.setGeometry(QRect(22, 40, 61, 21))
        font1 = QFont()
        font1.setPointSize(11)
        self.label_buildTip_5.setFont(font1)
        self.label_buildTip_5.setStyleSheet(u"")
        self.lineEdit_compared = QLineEdit(FilesMD5Snapshot)
        self.lineEdit_compared.setObjectName(u"lineEdit_compared")
        self.lineEdit_compared.setGeometry(QRect(90, 40, 311, 21))
        self.toolButton_compared = QToolButton(FilesMD5Snapshot)
        self.toolButton_compared.setObjectName(u"toolButton_compared")
        self.toolButton_compared.setGeometry(QRect(410, 40, 24, 21))
        self.lineEdit_search = QLineEdit(FilesMD5Snapshot)
        self.lineEdit_search.setObjectName(u"lineEdit_search")
        self.lineEdit_search.setGeometry(QRect(600, 10, 201, 21))
        self.lineEdit_search.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pushButton_search = QPushButton(FilesMD5Snapshot)
        self.pushButton_search.setObjectName(u"pushButton_search")
        self.pushButton_search.setGeometry(QRect(810, 10, 75, 23))
        self.radioButton_withJson = QRadioButton(FilesMD5Snapshot)
        self.radioButton_withJson.setObjectName(u"radioButton_withJson")
        self.radioButton_withJson.setGeometry(QRect(440, 40, 131, 20))
        self.pushButton_build = QPushButton(FilesMD5Snapshot)
        self.pushButton_build.setObjectName(u"pushButton_build")
        self.pushButton_build.setGeometry(QRect(810, 40, 75, 23))
        self.groupBox = QGroupBox(FilesMD5Snapshot)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 90, 891, 341))
        self.tableWidget_info = QTableWidget(self.groupBox)
        if (self.tableWidget_info.columnCount() < 4):
            self.tableWidget_info.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_info.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_info.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_info.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget_info.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tableWidget_info.setObjectName(u"tableWidget_info")
        self.tableWidget_info.setGeometry(QRect(10, 20, 871, 311))
        font2 = QFont()
        font2.setPointSize(10)
        self.tableWidget_info.setFont(font2)
        self.lineEdit_compared.raise_()
        self.pushButton_export.raise_()
        self.label_buildTip_4.raise_()
        self.toolButton_targetPath.raise_()
        self.label_buildTip_5.raise_()
        self.toolButton_compared.raise_()
        self.lineEdit_targetPath.raise_()
        self.lineEdit_search.raise_()
        self.pushButton_search.raise_()
        self.radioButton_withJson.raise_()
        self.pushButton_build.raise_()
        self.groupBox.raise_()

        self.retranslateUi(FilesMD5Snapshot)

        QMetaObject.connectSlotsByName(FilesMD5Snapshot)
    # setupUi

    def retranslateUi(self, FilesMD5Snapshot):
        FilesMD5Snapshot.setWindowTitle(QCoreApplication.translate("FilesMD5Snapshot", u"Form", None))
        self.lineEdit_targetPath.setPlaceholderText(QCoreApplication.translate("FilesMD5Snapshot", u"\u8f93\u5165\u751f\u6210\u5feb\u7167\u7684\u76ee\u7684\u6587\u4ef6\u5939\u8def\u5f84", None))
#if QT_CONFIG(tooltip)
        self.pushButton_export.setToolTip(QCoreApplication.translate("FilesMD5Snapshot", u"\u5bfc\u51fa\u5bf9\u6bd4\u7ed3\u679c\u5230json\u4e2d", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_export.setStatusTip(QCoreApplication.translate("FilesMD5Snapshot", u"\u5bfc\u51fa\u5bf9\u6bd4\u7ed3\u679c\u5230json\u4e2d", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_export.setText(QCoreApplication.translate("FilesMD5Snapshot", u"Export", None))
        self.label_buildTip_4.setText(QCoreApplication.translate("FilesMD5Snapshot", u"\u76ee\u6807\u8def\u5f84", None))
#if QT_CONFIG(tooltip)
        self.toolButton_targetPath.setToolTip(QCoreApplication.translate("FilesMD5Snapshot", u"\u9009\u62e9\u76ee\u6807\u8def\u5f84", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.toolButton_targetPath.setStatusTip(QCoreApplication.translate("FilesMD5Snapshot", u"\u9009\u62e9\u76ee\u6807\u8def\u5f84", None))
#endif // QT_CONFIG(statustip)
        self.toolButton_targetPath.setText(QCoreApplication.translate("FilesMD5Snapshot", u"...", None))
        self.label_buildTip_5.setText(QCoreApplication.translate("FilesMD5Snapshot", u"\u5bf9\u6bd4\u8def\u5f84", None))
        self.lineEdit_compared.setPlaceholderText(QCoreApplication.translate("FilesMD5Snapshot", u"\u8f93\u5165\u5bf9\u6bd4\u6587\u4ef6\u5939\u7684\u8def\u5f84\uff08\u975e\u5fc5\u9009\uff09", None))
#if QT_CONFIG(tooltip)
        self.toolButton_compared.setToolTip(QCoreApplication.translate("FilesMD5Snapshot", u"\u9009\u62e9\u5bf9\u6bd4\u8def\u5f84", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.toolButton_compared.setStatusTip(QCoreApplication.translate("FilesMD5Snapshot", u"\u9009\u62e9\u5bf9\u6bd4\u8def\u5f84", None))
#endif // QT_CONFIG(statustip)
        self.toolButton_compared.setText(QCoreApplication.translate("FilesMD5Snapshot", u"...", None))
        self.lineEdit_search.setPlaceholderText(QCoreApplication.translate("FilesMD5Snapshot", u"\u5728\u8868\u683c\u4e2d\u641c\u7d22", None))
#if QT_CONFIG(tooltip)
        self.pushButton_search.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButton_search.setText(QCoreApplication.translate("FilesMD5Snapshot", u"Search", None))
#if QT_CONFIG(tooltip)
        self.radioButton_withJson.setToolTip(QCoreApplication.translate("FilesMD5Snapshot", u"\u662f\u5426\u9700\u8981\u4e0ejson\u6587\u4ef6\u8fdb\u884c\u6bd4\u5bf9\uff0c\u800c\u975e\u67d0\u4e2a\u6587\u4ef6\u8def\u5f84", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.radioButton_withJson.setStatusTip(QCoreApplication.translate("FilesMD5Snapshot", u"\u662f\u5426\u9700\u8981\u4e0ejson\u6587\u4ef6\u8fdb\u884c\u6bd4\u5bf9\uff0c\u800c\u975e\u67d0\u4e2a\u6587\u4ef6\u8def\u5f84", None))
#endif // QT_CONFIG(statustip)
        self.radioButton_withJson.setText(QCoreApplication.translate("FilesMD5Snapshot", u"\u4e0eJson\u5bf9\u6bd4", None))
#if QT_CONFIG(tooltip)
        self.pushButton_build.setToolTip(QCoreApplication.translate("FilesMD5Snapshot", u"\u5bfc\u51fa\u76ee\u6807\u8def\u5f84\u4e2d\u5dee\u5f02\u5316\u7684\u6587\u4ef6\u5230\u8f93\u51fa\u8def\u5f84", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.pushButton_build.setStatusTip(QCoreApplication.translate("FilesMD5Snapshot", u"\u5bfc\u51fa\u76ee\u6807\u8def\u5f84\u4e2d\u5dee\u5f02\u5316\u7684\u6587\u4ef6\u5230\u8f93\u51fa\u8def\u5f84", None))
#endif // QT_CONFIG(statustip)
        self.pushButton_build.setText(QCoreApplication.translate("FilesMD5Snapshot", u"Build", None))
        self.groupBox.setTitle(QCoreApplication.translate("FilesMD5Snapshot", u"\u663e\u793a\u533a", None))
        ___qtablewidgetitem = self.tableWidget_info.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("FilesMD5Snapshot", u"\u6587\u4ef6\u540d", None));
        ___qtablewidgetitem1 = self.tableWidget_info.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("FilesMD5Snapshot", u"md5\u503c", None));
        ___qtablewidgetitem2 = self.tableWidget_info.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("FilesMD5Snapshot", u"\u5bf9\u6bd4md5\u503c", None));
        ___qtablewidgetitem3 = self.tableWidget_info.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("FilesMD5Snapshot", u"\u662f\u5426\u53d8\u66f4", None));
#if QT_CONFIG(tooltip)
        self.tableWidget_info.setToolTip(QCoreApplication.translate("FilesMD5Snapshot", u"\u70b9\u51fb\u8868\u5934\u53ef\u4ee5\u6309\u9875\u7b7e\u8fdb\u884c\u6392\u5e8f", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.tableWidget_info.setStatusTip(QCoreApplication.translate("FilesMD5Snapshot", u"\u70b9\u51fb\u8868\u5934\u53ef\u4ee5\u6309\u9875\u7b7e\u8fdb\u884c\u6392\u5e8f", None))
#endif // QT_CONFIG(statustip)
    # retranslateUi

