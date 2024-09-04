# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QWidget

# Important:
# You need to run the following command to generate the ui_mainwindow.py file
#     pyside6-uic form.ui -o ui_mainwindow.py, or
#     pyside2-uic form.ui -o ui_mainwindow.py
from sample.qt.src.widget.ui_ResConvertWidget import Ui_ResConvertWidget

import sample.src_references.common.g.G as G
import sample.src_references.Main as ToolsMain
import sample.src_references.common.vos.FoaBuildVO as KB_VO
import sample.src_references.common.utils.InputUtil as InputUtil
import sample.src_references.common.utils.FolderUtil as FolderUtil

ALL_PLATFORM_LANG = KB_VO.ALL_PLATFORM_LANG

class ResConvertWidget(QWidget):
    def __init__(self, uniqueKey, callback):
        super().__init__(parent=None)
        self._callback = callback
        self._inPath = None
        self._outPath = None
        self._pendingResources = {}
        self._processedResources = {}
        self._uniqueKey = uniqueKey
        self.paraVo = None
        self.ui = Ui_ResConvertWidget()
        self.ui.setupUi(self)
        self.initResConvertPage()
        G.getG('LogMgr').getLogger(self._uniqueKey).info(uniqueKey)

    def getUniqueKey(self):
        return self._uniqueKey

    def initResConvertPage(self):
        self.ui.pushButton_build.clicked[bool].connect(self.onClickBuild)
        self.ui.toolButton_inPath.clicked[bool].connect(self.onClickInPath)
        self.ui.toolButton_outPath.clicked[bool].connect(self.onClickOutPath)
        self.ui.toolButton_outPath_extra.clicked[bool].connect(self.onClickOutPathExtra)
        self.ui.lineEdit_inPath.textChanged.connect(self.onSetInPath)
        self.ui.lineEdit_outPath.textChanged.connect(self.onSetOutPath)
        self.ui.pushButton_emptyPending.clicked.connect(self.clearPendingList)
        self.ui.pushButton_emptyProcessed.clicked.connect(self.clearProcessedList)

        self.ui.listWidget_pending._signalDragEnterEvent.connect(lambda:self.ui.label_dropTips.setVisible(False))
        self.ui.listWidget_pending._signalDragEvent.connect(self.onDropEvent)
                 
        self.ui.comboBox_resPlatform.addItems(ALL_PLATFORM_LANG.values())


    def onDropEvent(self, urls):
        filesDict = {}
        for qUrl in urls:
            url = qUrl.toLocalFile()
            if FolderUtil.isDir(url):
                files = FolderUtil.getFilesInfo(url)
                self.updatePendingResources(files)
            else:
                fileName = FolderUtil.getUrlInfo(url)[0]
                filesDict[fileName] = url
        
        self.updatePendingResources(filesDict)
        self.ui.listWidget_pending.clear()
        self.ui.listWidget_pending.addItems(self._pendingResources.keys())
        self.checkDropTipsVisible()


    def updatePendingResources(self, filesDict):
        for fileName, url in filesDict.items():
            if self._pendingResources.get(fileName):
                G.getG('LogMgr').getLogger(self._uniqueKey).warning("文件%s已存在,进行替换" % fileName)
            self._pendingResources[fileName] = url


    def onClickInPath(self):
        inPath = InputUtil.InPutDirectoryGUI()
        if inPath == "":return
        self.ui.lineEdit_inPath.setText(inPath)

    def onClickOutPath(self):
        outPath = InputUtil.InPutDirectoryGUI()
        if outPath == "":return
        self.ui.lineEdit_outPath.setText(outPath)

    def onClickOutPathExtra(self):
        outPath = InputUtil.InPutDirectoryGUI()
        if outPath == "":return
        self.ui.lineEdit_outPath_extra.setText(outPath)

    def onSetInPath(self, path):
        if FolderUtil.exists(path):
            if path != None and self._inPath != path:
                self.refreshPendingList(path)

            self._inPath = path
            G.getG('LogMgr').getLogger(self._uniqueKey).info("成功设置输入路径:%s" % self._inPath)
        else:
            G.getG('LogMgr').getLogger(self._uniqueKey).warning("路径不存在:%s" % path)

    def onSetOutPath(self, path):
        if FolderUtil.exists(path):
            if path != None and self._outPath != path:
                self.refreshProcessedList(path)

            self._outPath = path
            G.getG('LogMgr').getLogger(self._uniqueKey).info("成功设置输出路径:%s" % self._inPath)
        else:
            G.getG('LogMgr').getLogger(self._uniqueKey).warning("路径:%s不存在:" % path)

    def clearPendingList(self):
        self._pendingResources = {}
        self.ui.lineEdit_inPath.clear()
        self.ui.listWidget_pending.clear()
        self.checkDropTipsVisible()

    def clearProcessedList(self):
        self._outPath = None
        self._processedResources = {}
        self.ui.lineEdit_outPath.clear()
        self.ui.listWidget_processed.clear()

    def checkDropTipsVisible(self):
        visible = self.ui.listWidget_pending.count() <= 0
        self.ui.label_dropTips.setVisible(visible)

    def refreshPendingList(self, path):
        filesDict = FolderUtil.getFilesInfo(path)
        self._pendingResources = filesDict
        self.ui.listWidget_pending.clear()
        self.ui.listWidget_pending.addItems(filesDict.keys())
        self.checkDropTipsVisible()

    def refreshProcessedList(self, path):        
        filesDict = FolderUtil.getFilesInfo(path)
        self._processedResources = filesDict
        self.ui.listWidget_processed.clear()
        self.ui.listWidget_processed.addItems(filesDict.keys())

    def getBuildDict(self):
        buildDict = {}
        opt = self._uniqueKey.split('-')[0]
        buildDict['opt'] = opt
        buildDict['sourceItems'] = self._pendingResources
        buildDict['inputUrl'] = self.ui.lineEdit_inPath.displayText()
        buildDict['outputUrl'] = self.ui.lineEdit_outPath.displayText()
        buildDict['outputUrlExtra'] = self.ui.lineEdit_outPath_extra.displayText()
        lang_platform = self.ui.comboBox_resPlatform.currentText()
        platform = list(ALL_PLATFORM_LANG.keys())[list(ALL_PLATFORM_LANG.values()).index(lang_platform)]
        buildDict['platform'] = platform

        return buildDict

    def getFuncOutPath(self):
        if self._outPath and FolderUtil.exists(self._outPath):
            return self._outPath
        RES_CONVERT_PATH = 'sample/output/'
        arr = self.getUniqueKey().split('-', 1)
        workDir = '%s/%s/%s/' %(RES_CONVERT_PATH, arr[0], arr[1])
        if not FolderUtil.exists(workDir):
            FolderUtil.create(workDir)
        return workDir

    def getVO(self):
        return self.paraVo

    def onClickBuild(self):
        paraDict = self.getBuildDict()
        self.paraVo = ToolsMain.inputByDict(paraDict)
        self.paraVo.setUniqueKey(self.getUniqueKey())
        self.paraVo.setFuncOutPath(self.getFuncOutPath())
        ToolsMain.main(self.paraVo)
        if self._outPath and FolderUtil.exists(self._outPath):
            self.refreshProcessedList(self._outPath)
        if self._callback:
            self._callback(self.getUniqueKey())