# This Python file uses the following encoding: utf-8
import os
import sys
import copy
import time
from pathlib import Path

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem

from sample.qt.src.common import Enum
import sample.src_references.common.g.G as G
import sample.src_references.common.utils.StringUtil as StringUtil

from sample.src_references.common.manager.LogMgr import LogMgr
from sample.src_references.common.manager.KBMgr import KBMgr

from sample.qt.src.ui_mainwindow import Ui_MainWindow
from sample.qt.src.pyui.QTextEditLogger import QTextEditLogger
from sample.qt.src.pyui.GridProgressBar import GridProgressBar
from sample.src_references.common.utils import TerminalUtil

ENUM_OPT_LANG = Enum.ENUM_OPT_LANG
ENUM_OPT_QTUI = Enum.ENUM_OPT_QTUI

class LogUpdateThread(QThread):
    log_updated = Signal(list)
    search_done = Signal(list)

    def __init__(self, uniqueKey, searchText=None):
        super().__init__()
        self.logMgr = G.getG('LogMgr')
        self.uniqueKey = uniqueKey
        self.searchText = searchText
        self._running = True  # 标志变量

    def run(self):
        if not self.uniqueKey:
            return
        log = self.logMgr.getLog(self.uniqueKey)
        buffer = []
        batch_size = 50  # 调整这个值以控制每批次更新的行数

        if self.searchText:
            filtered_log = [line for line in log if self.searchText in line]
            if self._running:
                self.search_done.emit(filtered_log)
        else:
            for line in log:
                if not self._running:  # 检查是否需要终止线程
                    break
                buffer.append(line)
                if len(buffer) >= batch_size:
                    self.log_updated.emit(buffer)
                    buffer = []
                QThread.msleep(1)  # 减少睡眠时间以提高更新速度

            if buffer:  # 发送剩余的日志
                self.log_updated.emit(buffer)

    def stop(self):  # 安全停止线程的方法
        self._running = False

class MainWindow(QMainWindow):
    progress_updated = Signal(int)
    prolist_item_added = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.uiWidgets = {}
        self.ui.setupUi(self)
        self.log_thread = None

        self.progress_updated.connect(self.onProgressBarValueChanged)
        self.prolist_item_added.connect(self.onListWidgetProgressItemAdded)

    def initUI(self):
        self.ui.textEditLogger = QTextEditLogger(self.ui.plainTextEdit_log, self)
        self.ui.plainTextEdit_log.document().setMaximumBlockCount(1000)  # 设置最大显示 1000 行
        self.setWindowTitle('KBTools')

        # 搜索功能
        self._funcSearchLine = None
        self._disableSearchLine = None
        self.setAvailableFuncs()
        self.ui.progressBar.setRange(0, 100)
        self.ui.progressBar.setValue(0)
        self.ui.progressWidget.update_progress(0)
        self.ui.listWidget_allFuncs.itemDoubleClicked.connect(self.onAllFuncsItemDoubleClicked)
        self.ui.lineEdit_funcSearch.textChanged[str].connect(self.onFuncSearchLineChanged)
        self.ui.checkBox_funcSearch.stateChanged.connect(self.onFuncSearchBoxChanged)
        self.ui.tabWidget_allFuncs.tabCloseRequested.connect(self.onFuncTabWidgetClose)
        self.ui.tabWidget_allFuncs.currentChanged.connect(self.onFuncTabWidgetCurrentChanged)
        self.ui.commandLinkButton.clicked[bool].connect(self.onCommandLinkButtonClicked)
        self.ui.lineEdit_logSearch.cursorPositionChanged.connect(self.onLogSearchLineChanged)
        self.ui.comboBox_allLogType.currentIndexChanged.connect(self.onLogTypeChanged)
        self.ui.commandLinkButton_log.clicked.connect(self.onCommandLinkButtonLogClicked)

    def onCommandLinkButtonClicked(self):
        try:
            tab = self.ui.tabWidget_allFuncs.currentWidget()
            displayUniqueKey = tab.getUniqueKey() if hasattr(tab, 'getUniqueKey') else None
            if not hasattr(tab, 'getFuncOutPath'):
                G.getG('LogMgr').getLogger(displayUniqueKey).info('前往失败,当前功能不支持这个选项')
            else:
                path = Path(tab.getFuncOutPath())
                if path.exists():
                    path = path.resolve()
                    os.startfile(str(path))
        except Exception as e:
            G.getG('LogMgr').getLogger(displayUniqueKey).error(f"Error opening path: {e}")

    def onCommandLinkButtonLogClicked(self):
        try:
            # 获取当前选项卡
            tab = self.ui.tabWidget_allFuncs.currentWidget()
            # 获取当前选项卡的唯一标识
            displayUniqueKey = tab.getUniqueKey() if hasattr(tab, 'getUniqueKey') else None

            if not displayUniqueKey:
                return
            # 获取日志文件路径
            logMgr = G.getG('LogMgr')
            logPath = logMgr.getLogUrl(displayUniqueKey)
            path = Path(logPath)

            if path.exists():
                # 如果日志文件存在，则打开文件
                path = path.resolve()
                # os.startfile(str(path))
                TerminalUtil.open_in_explorer(str(path))
            else:
                # 如果日志文件不存在，则记录警告
                logMgr.getLogger(displayUniqueKey).warning(f"日志文件不存在: {logPath}")
        except Exception as e:
            # 捕获异常并记录错误日志
            displayUniqueKey = displayUniqueKey if 'displayUniqueKey' in locals() else "Unknown"
            G.getG('LogMgr').getLogger(displayUniqueKey).error(f"打开日志文件时发生错误: {e}")

    def onFuncSearchLineChanged(self, text):
        self._funcSearchLine = text
        self.setAvailableFuncs()

    def onFuncSearchBoxChanged(self, state):
        self._disableSearchLine = state != Qt.CheckState.Checked.value
        self.setAvailableFuncs()

    def getUniqueKey(self, optKey):
        timeStr = time.strftime("%y%m%d%H%M_%S", time.localtime()) + str(int(time.time() * 1000000) % 1000000)
        return '%s-%s' % (optKey, timeStr)

    def onAllFuncsItemDoubleClicked(self):
        item = self.ui.listWidget_allFuncs.selectedItems()[0]
        optKey = list(ENUM_OPT_LANG.keys())[list(ENUM_OPT_LANG.values()).index(item.text())]
        optUI = ENUM_OPT_QTUI[optKey]
        module = __import__('sample.qt.src.widget.%s' % optUI, fromlist=[optUI])
        uiClass = getattr(module, optUI)
        uniqueKey = self.getUniqueKey(optKey)
        self.uiWidgets[uniqueKey] = uiClass(uniqueKey, self.onBuildFinish)

        index = self.ui.tabWidget_allFuncs.addTab(self.uiWidgets[uniqueKey], ENUM_OPT_LANG[optKey])
        self.ui.tabWidget_allFuncs.setCurrentIndex(index)

    def onFuncTabWidgetClose(self, index):
        self.ui.tabWidget_allFuncs.removeTab(index)

    def onFuncTabWidgetCurrentChanged(self, index):
        self.ui.label_funcTips.setVisible(index == -1)
        tab = self.ui.tabWidget_allFuncs.currentWidget()

        if not hasattr(tab, 'getUniqueKey'):
            uniqueKey = None
        else:
            uniqueKey = tab.getUniqueKey()
        self.refreshLogger(uniqueKey)
        self.refreshProgress(uniqueKey)
        self.refreshProList(uniqueKey)

        kbMgr = G.getG('KBMgr')
        # kbMgr.addGUIProCallback(lambda percent: self.progress_updated.emit(percent))
        # kbMgr.addGUIProListCallback(lambda item: self.prolist_item_added.emit(item))
        kbMgr.addGUIProCallback(lambda percent: self.onProgressBarValueChanged(percent))
        kbMgr.addGUIProListCallback(lambda item: self.onListWidgetProgressItemAdded(item))

    def onProgressBarValueChanged(self, value):
        self.ui.progressBar.setValue(value)
        self.ui.progressWidget.update_progress(value)

    def onListWidgetProgressItemAdded(self, item):
        # 遍历当前 listWidget 的所有项，检查是否已经存在
        items = [self.ui.listWidget_progress.item(i).text() for i in range(self.ui.listWidget_progress.count())]

        if item not in items:
            self.ui.listWidget_progress.addItem(item)
        else:
            print(f"Item '{item}' already exists in the list.")

    def setAvailableFuncs(self):
        self.ui.listWidget_allFuncs.clear()
        allFuncsDict = copy.copy(ENUM_OPT_LANG)
        allFuncs = ENUM_OPT_LANG.values()

        if self._funcSearchLine and len(self._funcSearchLine) > 0 and not self._disableSearchLine:
            for k, v in list(allFuncsDict.items()):
                if not StringUtil.PartialRatio(self._funcSearchLine, v, 80):
                    allFuncsDict.pop(k)
            allFuncs = allFuncsDict.values()

        for funName in allFuncs:
            font = QFont()
            font.setPointSize(11)
            item = QListWidgetItem(funName)
            item.setFont(font)
            self.ui.listWidget_allFuncs.addItem(item)

    def onBuildFinish(self, uniqueKey=None):
        G.getG('LogMgr').getLogger(uniqueKey).info('任务完成，执行回调')

    def refreshLogger(self, uniqueKey=None):
        if not uniqueKey:
            tab = self.ui.tabWidget_allFuncs.currentWidget()
            uniqueKey = tab.getUniqueKey() if hasattr(tab, 'getUniqueKey') else None
        self.ui.textEditLogger.setFuzzWord(None)

        self.ui.plainTextEdit_log.clear()
        self.ui.lineEdit_logSearch.clear()
        if not uniqueKey:
            self.ui.label_curFuncId.setText('空')
        else:
            type, id = uniqueKey.split('-')
            self.ui.label_curFuncId.setText('TYPE: ' + type + '\nID: ' + id)
            if self.log_thread:
                self.log_thread.stop()
                self.log_thread.wait()

            self.log_thread = LogUpdateThread(uniqueKey)
            self.log_thread.log_updated.connect(self.appendLogLines)
            self.log_thread.start()

    def onLogSearchLineChanged(self):
        text = self.ui.lineEdit_logSearch.text()
        self.ui.textEditLogger.setFuzzWord(text)
        if text:
            tab = self.ui.tabWidget_allFuncs.currentWidget()
            uniqueKey = tab.getUniqueKey() if hasattr(tab, 'getUniqueKey') else None
            self.log_thread = LogUpdateThread(uniqueKey, searchText=text)
            self.log_thread.search_done.connect(self.updateLogWithSearchResults)
            self.log_thread.start()
        else:
            self.refreshLogger()

    def onLogTypeChanged(self):
        text = self.ui.comboBox_allLogType.currentText()
        self.ui.textEditLogger.setFuzzWord(text)
        if text != "ALL":
            tab = self.ui.tabWidget_allFuncs.currentWidget()
            uniqueKey = tab.getUniqueKey() if hasattr(tab, 'getUniqueKey') else None
            self.log_thread = LogUpdateThread(uniqueKey, searchText=text)
            self.log_thread.search_done.connect(self.updateLogWithSearchResults)
            self.log_thread.start()
        else:
            self.refreshLogger()

    def updateLogWithSearchResults(self, filtered_log):
        self.ui.plainTextEdit_log.clear()
        for line in filtered_log:
            self.ui.plainTextEdit_log.appendPlainText(line)

    def appendLogLines(self, lines):
        if self.ui.lineEdit_logSearch.text():
            search_text = self.ui.lineEdit_logSearch.text()
            lines = [line for line in lines if search_text in line]
        if lines:
            combined_text = '\n'.join(lines)
            self.ui.plainTextEdit_log.appendPlainText(combined_text)

    def refreshProgress(self, uniqueKey=None):
        self.ui.progressBar.reset()
        self.ui.progressWidget.update_progress(0)
        if uniqueKey:
            percent = G.getG('KBMgr').getProgressNum(uniqueKey)
            self.ui.progressBar.setValue(percent)
            self.ui.progressWidget.update_progress(percent)

    def refreshProList(self, uniqueKey=None):
        if uniqueKey:
            proListInfo = G.getG('KBMgr').getProListInfo(uniqueKey)
            self.ui.listWidget_progress.clear()
            for item in proListInfo:
                self.ui.listWidget_progress.addItem(item.get('msg'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.initUI()
    widget.show()

    LogMgr(widget.ui.textEditLogger)
    kbMgr = KBMgr()
    G.setG('KBMgr', kbMgr)  # 确保在全局对象中设置 KBMgr 实例

    sys.exit(app.exec())
