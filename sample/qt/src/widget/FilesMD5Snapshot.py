# This Python file uses the following encoding: utf-8

from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QWidget, QHeaderView, QAbstractItemView, QMenu, QTableWidgetItem

# Important:
# You need to run the following command to generate the ui_mainwindow.py file
#     pyside6-uic form.ui -o ui_mainwindow.py, or
#     pyside2-uic form.ui -o ui_mainwindow.py
from sample.qt.src.widget.ui_FilesMD5Snapshot import Ui_FilesMD5Snapshot


import sample.src_references.common.utils.InputUtil as InputUtil
import sample.src_references.common.utils.FolderUtil as FolderUtil
import sample.src_references.common.utils.TerminalUtil as TerminalUtil
import sample.src_references.common.utils.Md5Util as Md5Util
import sample.src_references.common.utils.JsonUtil as JsonUtil
from sample.src_references.common.manager.LogMgr import LogMgr


class FilesMD5Snapshot(QWidget):
    def __init__(self, uniqueKey, callback):
        super().__init__(parent=None)
        self._callback = callback
        self.ui = Ui_FilesMD5Snapshot()
        self.ui.setupUi(self)
        self._uniqueKey = uniqueKey
        self.paraVo = None
        self.fileMd5Map = {}
        self._targetPath = None
        self._comparedPath = None
        self._order = None
        self._searchFlag = ["", -1]
        self.initFilesMD5SnapshotPage()
        self.logger = LogMgr.getLogger(self._uniqueKey)
        self.logger.info(uniqueKey)
        self.logger.info('点击表头可进行按列排序')


    def getUniqueKey(self):
        return self._uniqueKey

    def initFilesMD5SnapshotPage(self):
        self.ui.tableWidget_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.ui.tableWidget_info.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget_info.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableWidget_info.customContextMenuRequested.connect(self.generateMenu)
        self.ui.tableWidget_info.horizontalHeader().setSectionsClickable(True)
        self.ui.tableWidget_info.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)
        self.ui.lineEdit_targetPath.editingFinished.connect(self.onTargetPathEdited)
        self.ui.lineEdit_compared.editingFinished.connect(self.onComparedPathEdited)
        # self.ui.lineEdit_search.editingFinished.connect(self.onSearch)
        self.ui.pushButton_search.clicked[bool].connect(self.onSearch)
        self.ui.pushButton_export.clicked[bool].connect(self.onClickExport)
        self.ui.pushButton_build.clicked[bool].connect(self.onClickBuild)
        self.ui.toolButton_targetPath.clicked[bool].connect(self.onClickSetTargetPath)
        self.ui.toolButton_compared.clicked[bool].connect(self.onClickSetComparedPath)

    def onTargetPathEdited(self):
        targetPath = self.ui.lineEdit_targetPath.displayText()
        self.logger.info("目标路径:%s" % targetPath)
        if targetPath == "":
            self.clearTableWidget()
        else:
            self._targetPath = targetPath if targetPath != '' else None

    def onComparedPathEdited(self):
        comparedPath = self.ui.lineEdit_compared.displayText()
        if comparedPath == "":
            for key, val in self.fileMd5Map.items():
                self.fileMd5Map[key]['oMd5'] = None
                self.fileMd5Map[key]['oPath'] = None
            self.setTableWidget()
        else:
            self._comparedPath = comparedPath if comparedPath != '' else None

    def onSearch(self):
        matchText = self.ui.lineEdit_search.displayText()
        array = self.ui.tableWidget_info.findItems(matchText, Qt.MatchFlag.MatchContains)
        arrayLen = len(array)
        if matchText == "" or arrayLen <= 0 :return
        if self._searchFlag[0] == matchText:
            if self._searchFlag[1] < arrayLen-1:
                self._searchFlag[1] = self._searchFlag[1] + 1
            else:
                self._searchFlag[1] = 0
        else:
            self._searchFlag = [matchText, 0]
        self.ui.tableWidget_info.scrollToItem(array[self._searchFlag[1]], QAbstractItemView.ScrollHint.PositionAtCenter)
        self.ui.tableWidget_info.setCurrentItem(array[self._searchFlag[1]])
        self.logger.info("查找到%s个匹配项,当前为第%s个" % (arrayLen, self._searchFlag[1] + 1))


    def onHeaderClicked(self, index):
        if self._order == Qt.DescendingOrder:
            self.ui.tableWidget_info.sortItems(index, Qt.AscendingOrder)
            self._order = Qt.AscendingOrder
            self.logger.info("当前为第%s列,进行了升序排序" % index)
        else:
            self.ui.tableWidget_info.sortItems(index, Qt.DescendingOrder)
            self._order = Qt.DescendingOrder
            self.logger.info("当前为第%s列,进行了降序排序" % index)


    def generateMenu(self, pos):
        selections = []
        # 获取点击行号
        for i in self.ui.tableWidget_info.selectionModel().selection().indexes():
            rowNum = i.row()
            columnNum = i.column()
            selections.append([rowNum, columnNum])
        if len(selections) == 1 :
            self.onSingleSelMenu(pos, selections)
        elif len(selections) > 1 :
            self.onMultiSelMenu(pos, selections)


    def onSingleSelMenu(self, pos, selections):
        menu = QMenu()
        item1 = menu.addAction("复制")
        item2 = menu.addAction("在资源管理中打开")
        # 转换坐标系
        screenPos = self.ui.tableWidget_info.mapToGlobal(pos)
        # 被阻塞
        action = menu.exec(screenPos)
        rowNum = selections[0][0]
        columnNum = selections[0][1]
        if action == item1:
            selectdText = self.ui.tableWidget_info.item(rowNum, columnNum).text()
            TerminalUtil.ClipboardCopy(selectdText)
            print('copy:', selectdText)
        elif action == item2:
            print(self.ui.tableWidget_info.item(rowNum, columnNum).text())
        else:
            return

    def onMultiSelMenu(self, pos, selections):
        menu = QMenu()
        item1 = menu.addAction("导出所选文件")
        screenPos = self.ui.tableWidget_info.mapToGlobal(pos)
        action = menu.exec(screenPos)
        if action == item1:
            for selection in selections:
                filename = self.ui.tableWidget_info.item(selection[0], 0).text()
                path = self.fileMd5Map[filename].get('path')
                arr = path.split('XA/', 1)
                outputPath = self.getFuncOutPath() + arr[1]
                outUrl = FolderUtil.getUrlInfo(outputPath)[1]
                if not FolderUtil.exists(outUrl):
                    FolderUtil.create(outUrl)
                FolderUtil.copy(path, outUrl)
            self.logger.info("已成功导出%s项" % len(selections))
            self.logger.info("导出路径:%s" % (self.getFuncOutPath()))

    def getVO(self):
        return self.paraVo

    def onClickSetTargetPath(self):
        path = InputUtil.InPutDirectoryGUI()
        self._targetPath = path if path!='' else None
        if path == "":return
        self.logger.info("目标有效路径,正在计算md5值并显示,需要等待片刻")
        self.ui.lineEdit_targetPath.setText(path)
        self.updateMap(self._targetPath, self._comparedPath)

    def onClickSetComparedPath(self):
        isChecked = self.ui.radioButton_withJson.isChecked()
        if isChecked:
            path = InputUtil.InPutFilePathGUI()
        else:
            path = InputUtil.InPutDirectoryGUI()
        self._comparedPath = path if path != '' else None
        if path == "":return
        self.logger.info("对比有效路径,正在计算md5值并显示,需要等待片刻")
        self.ui.lineEdit_compared.setText(path)
        self.updateMap(self._targetPath, self._comparedPath)

    def updateMap(self,targetPath, comparedPath):
        self.logger.info("目标路径:%s" % self._targetPath)
        self.logger.info("对比路径:%s" % self._comparedPath)
        
        if targetPath :
            filesDict = FolderUtil.getFilesInfo(targetPath)
            self.fileMd5Map = Md5Util.fileTreeSnapshot(filesDict)
            if comparedPath:
                comparedMap = self.getComparedDict()
                for key, val in comparedMap.items():
                    if self.fileMd5Map.get(key):
                        self.fileMd5Map[key]['oMd5'] = val.get('md5')
                        self.fileMd5Map[key]['oPath'] = val.get('path')

        elif not targetPath and comparedPath:
            comparedMap = self.getComparedDict()
            self.fileMd5Map = {}
            for key, val in comparedMap.items():
                if not self.fileMd5Map.get(key):
                    self.fileMd5Map[key] = {}
                self.fileMd5Map[key]['oMd5'] = val.get('md5')
                self.fileMd5Map[key]['oPath'] = val.get('path')
        self.setTableWidget()

    def getComparedDict(self):
        if FolderUtil.exists(self._comparedPath):
            if FolderUtil.isDir(self._comparedPath):
                tDict = Md5Util.fileTreeSnapshot(FolderUtil.getFilesInfo(self._comparedPath))
                return tDict
            else:
                return JsonUtil.readDict(self._comparedPath)
        else:
            self.logger.info("对比文件不存在:%s" % self._comparedPath)


    def clearTableWidget(self):
        # self.logger.info("清空")
        self.ui.tableWidget_info.clear()
        self.ui.tableWidget_info.setRowCount(0)
        title1 = QCoreApplication.translate("FilesMD5Snapshot", u"\u6587\u4ef6\u540d", None)
        title2 = QCoreApplication.translate("FilesMD5Snapshot", u"md5\u503c", None)
        title3 = QCoreApplication.translate("FilesMD5Snapshot", u"\u5bf9\u6bd4md5\u503c", None)
        title4 = QCoreApplication.translate("FilesMD5Snapshot", u"\u662f\u5426\u53d8\u66f4", None)
        self.ui.tableWidget_info.setHorizontalHeaderLabels([title1,title2,title3,title4])

    def setTableWidget(self):
        self.clearTableWidget()
        self.ui.tableWidget_info.setRowCount(len(self.fileMd5Map))
        comparing = self._comparedPath != None
        i = 0
        for key, val in self.fileMd5Map.items():
            itemName = QTableWidgetItem(key)
            md5 = val.get('md5')
            oMd5 = val.get('oMd5')
            itemMd5 = QTableWidgetItem(md5)
            itemOMd5 = QTableWidgetItem(oMd5 if (oMd5 or not comparing) else 'deleted')
            if md5 and oMd5:
                if md5 == oMd5:
                    color = QColor(0,255-50,0)
                    itemIfSame = QTableWidgetItem('same')
                else:
                    color = QColor(255-50,0,0)
                    itemIfSame = QTableWidgetItem('different')
            else:
                colorInt = 205 if comparing else 255
                color = QColor(colorInt,colorInt,colorInt)
                itemIfSame = QTableWidgetItem('ignored' if comparing else '')

            itemIfSame.setBackground(QBrush(color))
            itemIfSame.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.ui.tableWidget_info.setItem(i, 0, itemName)
            self.ui.tableWidget_info.setItem(i, 1, itemMd5)
            self.ui.tableWidget_info.setItem(i, 2, itemOMd5)
            self.ui.tableWidget_info.setItem(i, 3, itemIfSame)
            i += 1

    def getFuncOutPath(self):
        SNAP_PATH = 'sample/output/'
        arr = self.getUniqueKey().split('-', 1)
        workDir = '%s/%s/%s/' %(SNAP_PATH, arr[0], arr[1])
        if not FolderUtil.exists(workDir):
            FolderUtil.create(workDir)
        return workDir

    def onClickExport(self):
        snapshotCfg = self.getFuncOutPath() + 'snapshot.json'
        JsonUtil.writeDict(self.fileMd5Map, snapshotCfg)
        self.logger.info("文件快照已导出至:%s" % snapshotCfg)
        if self._callback:
            self._callback(self.getUniqueKey())

    # 导出差异化的文件
    def onClickBuild(self):
        # print(self.fileMd5Map)
        for key, val in self.fileMd5Map.items():
            md5 = self.fileMd5Map[key].get('md5')
            oMd5 = self.fileMd5Map[key].get('oMd5')

            if md5 and oMd5 and md5 != oMd5:
                path = self.fileMd5Map[key].get('path')
                filePath = FolderUtil.getUrlInfo(path)[4]
                outPath = self.getFuncOutPath() + filePath
                if not FolderUtil.exists(outPath):
                    FolderUtil.create(outPath)
                FolderUtil.copy(path, outPath)
        self.logger.info("差异文件已导出,点击‘输出路径’前往查看")      