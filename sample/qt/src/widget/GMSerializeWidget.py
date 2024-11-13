from PySide6.QtWidgets import QWidget

from sample.qt.src.common import Enum
from sample.qt.src.widget.ui_GMSerializeWidget import Ui_GMSerializeWidget

import sample.src_references.common.g.G as G
import sample.src_references.Main as ToolsMain
import sample.src_references.common.utils.FolderUtil as FolderUtil

class GMSerializeWidget(QWidget):
    def __init__(self, uniqueKey, callback):
        super().__init__(parent=None)
        self._callback = callback
        self._inPath = None
        self._pendingResources = {}
        self._processedResources = {}
        self._uniqueKey = uniqueKey
        self.paraVo = None
        self.ui = Ui_GMSerializeWidget()
        self.ui.setupUi(self)
        self.initDetectDuplicateFilesUI()
        G.getG('LogMgr').getLogger(self._uniqueKey).info(uniqueKey)

    def getFuncOutPath(self):
        FOA_BUILD_PATH = 'sample/output/'
        arr = self.getUniqueKey().split('-', 1)
        workDir = '%s/%s/%s/' % (FOA_BUILD_PATH, arr[0], arr[1])
        if not FolderUtil.exists(workDir):
            FolderUtil.create(workDir)
        return workDir

    def getUniqueKey(self):
        return self._uniqueKey

    def initDetectDuplicateFilesUI(self):
        self.ui.pushButton_build.clicked[bool].connect(self.onClickBuild)

        self.ui.listWidget_pending._signalDragEnterEvent.connect(lambda: self.ui.label_dropTips.setVisible(False))
        self.ui.listWidget_pending._signalDragEvent.connect(self.onDropEvent)

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
                G.getG('LogMgr').getLogger(self._uniqueKey).warning("文件%s已存在,进行地址更新" % fileName)
            self._pendingResources[fileName] = url

    def clearPendingList(self):
        self._pendingResources = {}
        self.ui.listWidget_pending.clear()
        self.checkDropTipsVisible()

    def clearProcessedList(self):
        self._processedResources = {}
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
        buildDict['opt'] = Enum.ENUM_OPT.get(opt)
        buildDict['sourceItems'] = self._pendingResources

        return buildDict

    def getVO(self):
        return self.paraVo

    def onClickBuild(self):

        paraDict = self.getBuildDict()
        self.paraVo = ToolsMain.inputByDict(paraDict)
        self.paraVo.setUniqueKey(self.getUniqueKey())
        self.paraVo.setFuncOutPath(self.getFuncOutPath())

        errors = ToolsMain.main(self.paraVo)
        self.refreshProcessedList(self.getFuncOutPath())
        if self._callback:
            self._callback(self.getUniqueKey())