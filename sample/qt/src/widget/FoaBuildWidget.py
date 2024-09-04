# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QWidget, QMessageBox

# Important:
# You need to run the following command to generate the ui_mainwindow.py file
#     pyside6-uic form.ui -o ui_mainwindow.py, or
#     pyside2-uic form.ui -o ui_mainwindow.py
from sample.qt.src.widget.ui_FoaBuildWidget import Ui_FoaBuildWidget

from sample.qt.src.widget.QuicParasAddTips import QuicParasAddTips

import sample.src_references.common.g.G as G
import sample.src_references.Main as ToolsMain
import sample.src_references.common.utils.InputUtil as InputUtil
import sample.src_references.common.utils.JsonUtil as JsonUtil
import sample.src_references.common.utils.StringUtil as StringUtil
import sample.src_references.common.utils.FolderUtil as FolderUtil
import sample.src_references.common.vos.FoaBuildVO as KB_VO
FOA_BUILD_VO = KB_VO.FOA_BUILD_VO
ALL_PLATFORM_LANG = KB_VO.ALL_PLATFORM_LANG
ALL_BRANCHES_REPO = KB_VO.ALL_BRANCHES_REPO

class FoaBuildWidget(QWidget):
    def __init__(self, uniqueKey, callback):
        super().__init__(parent=None)
        self._callback = callback
        self.ui = Ui_FoaBuildWidget()
        self.ui.setupUi(self)
        self.initFoaPage()
        self._uniqueKey = uniqueKey
        self._snapshopPath = None
        self._outPath1 = None
        self._outPath2 = None
        self.paraVo = None
        G.getG('LogMgr').getLogger(self._uniqueKey).info(uniqueKey)

    def getUniqueKey(self):
        return self._uniqueKey
        
    def initFoaPage(self):
        self.ui.pushButton_build.clicked[bool].connect(self.onClickBuild)
        self.ui.toolButton_pathSet.clicked[bool].connect(self.onClickPathSet)
        self.ui.lineEdit_pathSet.textChanged.connect(self.onPathSet)
        self.ui.toolButton_quicParasAdd.clicked[bool].connect(self.onClickQuicParasAdd)
        self.ui.toolButton_quicParasSync.clicked[bool].connect(self.onClickQuicParasSync)
        self.ui.toolButton_quicParasDel.clicked[bool].connect(self.onClickQuicParasDel)
        self.ui.comboBox_allBranches.currentTextChanged.connect(self.onComboBoxChanged)
        self.ui.comboBox_platform.currentTextChanged.connect(self.onComboBoxChanged)
        self.ui.comboBox_quicParas.currentTextChanged.connect(self.onParasBoxChanged)

        self.ui.lineEdit_snapshot.textChanged.connect(self.onSnapshotPathChanged)
        self.ui.comboBox_allBranches.addItems(ALL_BRANCHES_REPO.keys())
        self.ui.toolButton_snapshotSet.clicked[bool].connect(self.onClickSnapshotSet)
        self.ui.radioButton_snapshot.clicked[bool].connect(self.onClickSwitchSnapshot)

        self.ui.lineEdit_outPath1.textChanged.connect(self.onOutPath1Changed)
        self.ui.lineEdit_outPath2.textChanged.connect(self.onOutPath2Changed)
        self.ui.toolButton_outPath1.clicked[bool].connect(self.onClickOutPath1)
        self.ui.toolButton_outPath2.clicked[bool].connect(self.onClickOutPath2)

        self.setBuildDefault()
        self.refreshQuicParasComboBox()

    def onOutPath1Changed(self):
        if self.ui.lineEdit_outPath1.displayText() == "":
            self._outPath1 = ""
            self.syncSnapshotCfg()

    def onOutPath2Changed(self):
        if self.ui.lineEdit_outPath2.displayText() == "":
            self._outPath2 = ""
            self.syncSnapshotCfg()

    def onClickOutPath1(self):
        outPath = InputUtil.InPutDirectoryGUI()
        if outPath == "":return
        self._outPath1 = outPath
        self.ui.lineEdit_outPath1.setText(outPath)
        self.syncSnapshotCfg()

    def onClickOutPath2(self):
        outPath = InputUtil.InPutDirectoryGUI()
        if outPath == "":return
        self._outPath2 = outPath
        self.ui.lineEdit_outPath2.setText(outPath)
        self.syncSnapshotCfg()


    def onSnapshotPathChanged(self):
        self.syncSnapshotCfg()

    def onClickSnapshotSet(self):
        outPath = InputUtil.InPutFilePathGUI()
        if outPath == "":return
        self.syncSnapshotCfg()
        self._snapshopPath = outPath
        self.ui.lineEdit_snapshot.setText(outPath)

    def syncSnapshotCfg(self):
        branch = self.ui.comboBox_allBranches.currentText()
        platform = self.ui.comboBox_platform.currentText()
        snapshotBinding = JsonUtil.readInCfg('snapshot_binding') or {}
        bindingInfo = snapshotBinding.get(branch) or {}
        bindingInfo['check'] = self.ui.radioButton_snapshot.isChecked()
        bindingInfo['cfgPath_%s'%platform] = self.ui.lineEdit_snapshot.displayText()
        bindingInfo['foa_outpath1'] = self.ui.lineEdit_outPath1.displayText()
        bindingInfo['foa_outpath2'] = self.ui.lineEdit_outPath2.displayText()
        snapshotBinding[branch] = bindingInfo
        JsonUtil.saveInCfg('snapshot_binding', snapshotBinding)

    def onClickSwitchSnapshot(self):
        self.syncSnapshotCfg()
        isChecked = self.ui.radioButton_snapshot.isChecked()
        if not isChecked:
            self.ui.lineEdit_snapshot.clear()
        else:
            branch = self.ui.comboBox_allBranches.currentText()
            snapshotBinding = JsonUtil.readInCfg('snapshot_binding') or {}
            bindingInfo = snapshotBinding.get(branch)
            if bindingInfo:
                platform = self.ui.comboBox_platform.currentText()
                self.ui.lineEdit_snapshot.setText(bindingInfo.get('cfgPath_%s'%platform))
            else:
                self.ui.lineEdit_snapshot.setText('')
            


    def refreshQuicParasComboBox(self):
        self.ui.comboBox_quicParas.clear()
        ALL_PARAS = JsonUtil.read(JsonUtil.PARAS)
        self.ui.comboBox_quicParas.addItems(ALL_PARAS.keys())
        if len(ALL_PARAS.keys()) <= 0:
            self.setBuildView({})
            self.setBuildDefault()

    def onQuicParasAddAccepted(self, name):
        self.refreshQuicParasComboBox()
        self.ui.comboBox_quicParas.setCurrentText(name)

    def onClickQuicParasAdd(self):
        self.ui.TipsDialog = QuicParasAddTips(self.onQuicParasAddAccepted)
        self.ui.TipsDialog.show()

    def onParasBoxChanged(self):
        name = self.ui.comboBox_quicParas.currentText()
        if not name:return
        paraVo = JsonUtil.readIn(JsonUtil.PARAS, name)
        self.setBuildView(paraVo)

    def onClickQuicParasSync(self):
        name = self.ui.comboBox_quicParas.currentText()
        if name == "":
            QMessageBox.warning(self, "同步失败", "请先添加一条快速参数")
            # G.getG('LogMgr').getLogger(self._uniqueKey).info('快速参数设置同步失败，请先添加一条快速参数')
        else:
            paraDict = self.getBuildDict()
            self.paraVo = ToolsMain.inputByDict(paraDict)
            JsonUtil.saveIn(JsonUtil.PARAS, name, self.paraVo.getAll())

    def onClickQuicParasDel(self):
        name = self.ui.comboBox_quicParas.currentText()
        JsonUtil.deleteIn(JsonUtil.PARAS, name)
        self.refreshQuicParasComboBox()


    def onComboBoxChanged(self):
        self.ui.lineEdit_pathSet.clear()
        branch = self.ui.comboBox_allBranches.currentText()
        platform = self.ui.comboBox_platform.currentText()
        path = G.getG("KBMgr").getBranchUrl(branch)
        if path:
            self.ui.lineEdit_pathSet.setText(path)

        snapshotBinding = JsonUtil.readInCfg('snapshot_binding') or {}
        bindingInfo = snapshotBinding.get(branch)
        if bindingInfo:
            self.ui.radioButton_snapshot.setChecked(bindingInfo.get('check'))
            self.ui.lineEdit_snapshot.setText(bindingInfo.get('cfgPath_%s'%platform))

            self.ui.lineEdit_outPath1.setText(bindingInfo.get('foa_outpath1'))
            self.ui.lineEdit_outPath2.setText(bindingInfo.get('foa_outpath2'))
        else:
            self.ui.radioButton_snapshot.setChecked(False)
            self.ui.lineEdit_snapshot.setText('')
            self.ui.lineEdit_outPath1.setText('')
            self.ui.lineEdit_outPath2.setText('')

    def onClickPathSet(self):
        path = InputUtil.InPutDirectoryGUI()
        if path == "":return
        self.ui.lineEdit_pathSet.setText(path)
        branch = self.ui.comboBox_allBranches.currentText()
        # branches = JsonUtil.readInCfg("branches") or {}
        # branches[branch] = path
        # JsonUtil.saveInCfg("branches", branches)
        G.getG("KBMgr").setBranchUrl(branch, path)

    def onPathSet(self):
        path = self.ui.lineEdit_pathSet.displayText()
        if path == "":return
        branch = self.ui.comboBox_allBranches.currentText()
        # branches = JsonUtil.readInCfg("branches") or {}
        # branches[branch] = path
        # JsonUtil.saveInCfg("branches", branches)
        G.getG("KBMgr").setBranchUrl(branch, path)

    def setBuildDefault(self):
        ALL_PARAS = JsonUtil.read(JsonUtil.PARAS)
        if len(ALL_PARAS.keys()) > 0:
            return
        self.ui.lineEdit_bigversion.setPlaceholderText(FOA_BUILD_VO['bigversion'])
        self.ui.lineEdit_channel.setPlaceholderText(FOA_BUILD_VO['channel'])
        self.ui.lineEdit_foaName.setPlaceholderText(FOA_BUILD_VO['foaName'])
        self.ui.lineEdit_focName.setPlaceholderText(FOA_BUILD_VO['focName'])
        self.ui.lineEdit_sysversion.setPlaceholderText(FOA_BUILD_VO['sysversion'])

        self.ui.comboBox_isDebug.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['isdebug']))
        self.ui.comboBox_sandBox.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['sandbox']))
        self.ui.comboBox_useLocals.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['use_localserverlist']))
        self.ui.comboBox_useSDK.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['use_sdk']))
        self.ui.comboBox_testapp.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['istestapp']))
        self.ui.comboBox_appstore.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['isAppleStoreReview']))

        self.ui.comboBox_lang.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['lang']))
        self.ui.comboBox_platform.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['platform']))
        self.ui.comboBox_is64.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['is64']))
        self.ui.lineEdit_targetRes.setPlaceholderText(FOA_BUILD_VO['res_target'])


    def setBuildView(self, buildDict):
        self.ui.lineEdit_bigversion.setText(buildDict.get('bigversion'))
        self.ui.lineEdit_channel.setText(buildDict.get('channel'))
        self.ui.lineEdit_foaName.setText(buildDict.get('foaName'))
        self.ui.lineEdit_focName.setText(buildDict.get('focName'))
        self.ui.lineEdit_sysversion.setText(buildDict.get('sysversion'))

        self.ui.comboBox_isDebug.setCurrentText(
            StringUtil.Py2LuaBool(buildDict.get('isdebug') or FOA_BUILD_VO['isdebug']))
        self.ui.comboBox_sandBox.setCurrentText(
            StringUtil.Py2LuaBool(buildDict.get('sandbox') or FOA_BUILD_VO['sandbox']))
        self.ui.comboBox_useLocals.setCurrentText(
            StringUtil.Py2LuaBool(buildDict.get('use_localserverlist') or FOA_BUILD_VO['use_localserverlist']))
        self.ui.comboBox_useSDK.setCurrentText(StringUtil.Py2LuaBool(buildDict.get('use_sdk') or FOA_BUILD_VO['use_sdk']))
        self.ui.comboBox_testapp.setCurrentText(
            StringUtil.Py2LuaBool(buildDict.get('istestapp') or FOA_BUILD_VO['istestapp']))
        self.ui.comboBox_appstore.setCurrentText(
            StringUtil.Py2LuaBool(buildDict.get('isAppleStoreReview') or FOA_BUILD_VO['isAppleStoreReview']))

        self.ui.comboBox_lang.setCurrentText(StringUtil.Py2LuaBool(buildDict.get('lang') or FOA_BUILD_VO['lang']))
        self.ui.comboBox_platform.setCurrentText(
            StringUtil.Py2LuaBool(buildDict.get('platform') or FOA_BUILD_VO['platform']))
        self.ui.comboBox_is64.setCurrentText(StringUtil.Py2LuaBool(buildDict.get('is64') or FOA_BUILD_VO['is64']))
        self.ui.lineEdit_targetRes.setText(buildDict.get('res_target'))


    def getBuildDict(self):
        buildDict = {}
        opt = self._uniqueKey.split('-')[0]
        buildDict['opt'] = opt
        buildDict['bigversion'] = self.ui.lineEdit_bigversion.displayText()
        buildDict['branches'] = self.ui.comboBox_allBranches.currentText()
        buildDict['channel'] = self.ui.lineEdit_channel.displayText()
        buildDict['foaName'] = self.ui.lineEdit_foaName.displayText()
        buildDict['focName'] = self.ui.lineEdit_focName.displayText()
        buildDict['sysversion'] = self.ui.lineEdit_sysversion.displayText()
        buildDict['tag'] = self.ui.lineEdit_channel.displayText()
        res_target = self.ui.lineEdit_targetRes.displayText()
        buildDict['snapshopPath'] = self.ui.lineEdit_snapshot.displayText()
        buildDict['outPath1'] = self.ui.lineEdit_outPath1.displayText()
        buildDict['outPath2'] = self.ui.lineEdit_outPath2.displayText()
        buildDict['res_target'] = None if res_target == "" else res_target

        buildDict['isdebug'] = StringUtil.Lua2PyBool(self.ui.comboBox_isDebug.currentText())
        buildDict['sandbox'] = StringUtil.Lua2PyBool(self.ui.comboBox_sandBox.currentText())
        buildDict['use_localserverlist'] = StringUtil.Lua2PyBool(self.ui.comboBox_useLocals.currentText())
        buildDict['use_sdk'] = StringUtil.Lua2PyBool(self.ui.comboBox_useSDK.currentText())
        buildDict['istestapp'] = StringUtil.Lua2PyBool(self.ui.comboBox_testapp.currentText())
        buildDict['isAppleStoreReview'] = StringUtil.Lua2PyBool(self.ui.comboBox_appstore.currentText())

        buildDict['lang'] = StringUtil.Lua2PyBool(self.ui.comboBox_lang.currentText())
        buildDict['platform'] = StringUtil.Lua2PyBool(self.ui.comboBox_platform.currentText())
        buildDict['is64'] = StringUtil.Lua2PyBool(self.ui.comboBox_is64.currentText())
        

        return buildDict

    def getFuncOutPath(self):
        FOA_BUILD_PATH = 'sample/output/'
        arr = self.getUniqueKey().split('-', 1)
        workDir = '%s/%s/%s/' %(FOA_BUILD_PATH, arr[0], arr[1])
        if not FolderUtil.exists(workDir):
            FolderUtil.create(workDir)
        return workDir

    def getVO(self):
        return self.paraVo

    def onClickBuild(self):
        paraDict = self.getBuildDict()
        G.getG('LogMgr').getLogger(self._uniqueKey).info('开始获取build参数')
        self.paraVo = ToolsMain.inputByDict(paraDict)
        self.paraVo.setUniqueKey(self.getUniqueKey())
        self.paraVo.setFuncOutPath(self.getFuncOutPath())

        # 校验
        branches = self.paraVo.getVal("branches")
        XA_Url = G.getG("KBMgr").getBranchUrl(branches)
        res_target = self.paraVo.getVal("res_target")
        platformRes = XA_Url +'/' + res_target
        if not FolderUtil.exists(platformRes):
            QMessageBox.warning(self, "目标资源不存在", "分支%s的工程路径中，没有文件夹:%s\n请修改参数面板中目标资源\n或者检查工程路径中的指定文件夹" % (branches, res_target))
            return

        snapshopPath = self.paraVo.getVal("snapshopPath")
        if not FolderUtil.exists(snapshopPath):
            self.ui.radioButton_snapshot.setChecked(False)
            self.ui.lineEdit_snapshot.setText('')
            G.getG('LogMgr').getLogger(self._uniqueKey).warning('文件快照不存在,此次构建取消自动化转资源:%s' % snapshopPath)


        foaErrors = ToolsMain.main(self.paraVo)
        if not foaErrors:
            G.getG('LogMgr').getLogger(self._uniqueKey).info("构建成功")
            QMessageBox.information(self, "构建成功", "构建成功")

        if self._callback:
            self._callback(self.getUniqueKey())