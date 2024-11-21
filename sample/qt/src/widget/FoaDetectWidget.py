from PySide6.QtWidgets import QWidget

from sample.qt.src.common import Enum
from sample.qt.src.widget.ui_FoaDetectWidget import Ui_FoaDetectWidget


import sample.src_references.Main as ToolsMain
import sample.src_references.common.utils.InputUtil as InputUtil
import sample.src_references.common.utils.FolderUtil as FolderUtil
from sample.src_references.common.manager.LogMgr import LogMgr


class FoaDetectWidget(QWidget):
    def __init__(self, uniqueKey, callback):
        super().__init__(parent=None)
        self._callback = callback
        self._inPath = None
        self._pendingResources = {}
        self._processedResources = {}
        self._uniqueKey = uniqueKey
        self.paraVo = None
        self.ui = Ui_FoaDetectWidget()
        self.ui.setupUi(self)
        self.initDetectDuplicateFilesUI()
        self.logger = LogMgr.getLogger(self._uniqueKey)
        self.logger.info(uniqueKey)

    def getFuncOutPath(self):
        FOA_BUILD_PATH = 'sample/output/'
        arr = self.getUniqueKey().split('-', 1)
        workDir = '%s/%s/%s/' %(FOA_BUILD_PATH, arr[0], arr[1])
        if not FolderUtil.exists(workDir):
            FolderUtil.create(workDir)
        return workDir

    def getUniqueKey(self):
        return self._uniqueKey

    def initDetectDuplicateFilesUI(self):
        self.ui.pushButton_build.clicked[bool].connect(self.onClickBuild)

        self.ui.toolButton_inPath.clicked[bool].connect(self.onClickInPath)
        self.ui.lineEdit_inPath.textChanged.connect(self.onSetInPath)
        self.ui.pushButton_emptyPending.clicked.connect(self.clearPendingList)

        self.ui.listWidget_pending._signalDragEnterEvent.connect(lambda:self.ui.label_dropTips.setVisible(False))
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
                self.logger.warning("文件%s已存在,进行地址更新" % fileName)
            self._pendingResources[fileName] = url


    def onClickInPath(self):
        inPath = InputUtil.InPutDirectoryGUI()
        if inPath == "":return
        self.ui.lineEdit_inPath.setText(inPath)

    def onSetInPath(self, path):
        if FolderUtil.exists(path):
            if path != None and self._inPath != path:
                self.refreshPendingList(path)

            self._inPath = path
            self.logger.info("成功设置输入路径:%s" % self._inPath)
        else:
            self.logger.warning("路径不存在:%s" % path)

    def clearPendingList(self):
        self._pendingResources = {}
        self.ui.lineEdit_inPath.clear()
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

    def refreshProcessedList(self, errors):
        errors = errors if errors else []
        self._processedResources = errors
        self.ui.listWidget_processed.clear()
        self.ui.listWidget_processed.addItems(errors)

    def getBuildDict(self):
        buildDict = {}
        opt = self._uniqueKey.split('-')[0]
        buildDict['opt'] = Enum.ENUM_OPT.get(opt)
        buildDict['sourceItems'] = self._pendingResources
        buildDict['inputUrl'] = self.ui.lineEdit_inPath.displayText()

        return buildDict


    def getVO(self):
        return self.paraVo

    def onClickBuild(self):

        paraDict = self.getBuildDict()
        self.paraVo = ToolsMain.inputByDict(paraDict)
        self.paraVo.setUniqueKey(self.getUniqueKey())
        self.paraVo.setFuncOutPath(self.getFuncOutPath())

        errors = ToolsMain.main(self.paraVo)
        self.refreshProcessedList(errors)
        if self._callback:
            self._callback(self.getUniqueKey())