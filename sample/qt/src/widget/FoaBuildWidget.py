from PySide6.QtWidgets import QWidget, QMessageBox, QComboBox, QListView, QMenu
from PySide6.QtGui import QCursor, QAction
from PySide6.QtCore import Qt

from sample.qt.src.common.AdminAuthManager import AuthManager
from sample.qt.src.pyui.BatchBuildDialog import BatchBuildDialog
from sample.qt.src.widget.ui_FoaBuildWidget import Ui_FoaBuildWidget
from sample.qt.src.widget.QuicParasAddTips import QuicParasAddTips

import sample.src_references.Main as ToolsMain
import sample.src_references.common.utils.InputUtil as InputUtil
import sample.src_references.common.utils.JsonUtil as JsonUtil
import sample.src_references.common.utils.StringUtil as StringUtil
import sample.src_references.common.utils.FolderUtil as FolderUtil
import sample.src_references.common.utils.TerminalUtil as TerminalUtil
import sample.src_references.common.vos.FoaBuildVO as KB_VO
from sample.src_references.common.manager.LogMgr import LogMgr
from sample.src_references.common.utils import Md5Util
from sample.src_references.common.manager.KBMgr import KBMgr

import os

# 从导入的模块中获取常量
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
        self._snapshotPath = None
        self.paraVo = None
        self.batchBuildDialog = None  # 初始化批量构建对话框
        self.logger = LogMgr.getLogger(self._uniqueKey)
        self.logger.info(uniqueKey)

    def getUniqueKey(self):
        return self._uniqueKey

    def initFoaPage(self):
        """初始化UI组件并连接信号与槽。"""
        # 连接信号与槽
        self.ui.pushButton_build.clicked.connect(self.onClickBuild)
        self.ui.toolButton_pathSet.clicked.connect(self.onClickPathSet)
        self.ui.lineEdit_pathSet.textChanged.connect(self.onPathSet)
        self.ui.toolButton_quicParasAdd.clicked.connect(self.onClickQuicParasAdd)
        self.ui.toolButton_quicParasSync.clicked.connect(self.onClickQuicParasSync)
        self.ui.toolButton_quicParasDel.clicked.connect(self.onClickQuicParasDel)
        self.ui.comboBox_allBranches.currentTextChanged.connect(self.onComboBoxChanged)
        self.ui.comboBox_platform.currentTextChanged.connect(self.onComboBoxChanged)
        self.ui.comboBox_quicParas.currentTextChanged.connect(self.onParasBoxChanged)

        # 初始化 comboBox_snapshot
        self.ui.comboBox_snapshot.clear()
        self.ui.comboBox_snapshot.setView(QListView())  # 设置自定义视图以支持右键菜单
        self.ui.comboBox_snapshot.view().setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.comboBox_snapshot.view().customContextMenuRequested.connect(self.onSnapshotItemRightClicked)
        self.ui.comboBox_snapshot.currentTextChanged.connect(self.onSnapshotPathChanged)
        self.ui.comboBox_allBranches.addItems(ALL_BRANCHES_REPO.keys())
        self.ui.toolButton_snapshotSet.clicked.connect(self.onClickSnapshotSet)
        self.ui.radioButton_snapshot.clicked.connect(self.onClickSwitchSnapshot)

        # 设置comboBox_snapshot的文本对齐方式为右对齐
        self.ui.comboBox_snapshot.setEditable(True)
        self.ui.comboBox_snapshot.lineEdit().setReadOnly(True)
        self.ui.comboBox_snapshot.lineEdit().setAlignment(Qt.AlignRight)

        # 处理输出路径的变化

        self.ui.toolButton_outPath1.clicked.connect(self.onClickOutPath)
        self.ui.toolButton_outPath2.clicked.connect(self.onClickOutPath)

        # 连接批量构建的信号
        self.ui.radioButton_batchBuild.toggled.connect(self.onBatchBuildToggled)
        self.ui.radioButton_batchBuild.setAutoExclusive(False)

        self.setBuildDefault()
        self.refreshQuicParasComboBox()

    def onBatchBuildToggled(self, checked):
        if checked:
            # 显示批量构建对话框
            self.batchBuildDialog = BatchBuildDialog(self)
            self.batchBuildDialog.show()
        else:
            # 关闭批量构建对话框
            if self.batchBuildDialog:
                self.batchBuildDialog.close()
                self.batchBuildDialog = None

    def onClickOutPath(self):
        """处理输出路径按钮的点击事件。"""
        sender = self.sender()
        outPath = InputUtil.InPutDirectoryGUI()
        if not outPath:
            return
        if sender == self.ui.toolButton_outPath1:
            self.ui.lineEdit_outPath1.setText(outPath)
        elif sender == self.ui.toolButton_outPath2:
            self.ui.lineEdit_outPath2.setText(outPath)

    def onSnapshotPathChanged(self):
        """当快照路径选择变化时更新快照路径。"""
        current_snapshot = self.ui.comboBox_snapshot.currentText()
        if current_snapshot:
            # 从用户数据中获取完整路径
            index = self.ui.comboBox_snapshot.currentIndex()
            self._snapshotPath = self.ui.comboBox_snapshot.itemData(index, Qt.UserRole)
            # 如果radioButton_snapshot未被勾选，勾选它
            if not self.ui.radioButton_snapshot.isChecked():
                self.ui.radioButton_snapshot.setChecked(True)
        else:
            self._snapshotPath = None
        self.syncSnapshotCfg()

    def onClickSnapshotSet(self):
        """处理设置快照路径的点击事件。"""
        outPath = InputUtil.InPutFilePathGUI()
        if not outPath:
            return
        branch = self.ui.comboBox_allBranches.currentText()
        platform = self.ui.comboBox_platform.currentText()
        snapshot_environment = JsonUtil.readInCfg('environment').get('snapshot')
        branch_platform = f'{branch}_{platform}'
        snapshot_cfg_path = FolderUtil.join(snapshot_environment, branch_platform)
        FolderUtil.copy(outPath, snapshot_cfg_path)
        self.displaySnapshot()
        self.syncSnapshotCfg()

    def syncSnapshotCfg(self):
        """同步快照配置。"""
        branch = self.ui.comboBox_allBranches.currentText()
        platform = self.ui.comboBox_platform.currentText()
        snapshot_binding = JsonUtil.readInCfg('snapshot_binding') or {}
        binding_info = snapshot_binding.get(branch) or {}
        binding_info['check'] = self.ui.radioButton_snapshot.isChecked()
        binding_info[f'snapshot_{platform}'] = self._snapshotPath
        snapshot_binding[branch] = binding_info
        JsonUtil.saveInCfg('snapshot_binding', snapshot_binding)

    def onClickSwitchSnapshot(self):
        """处理快照开关的切换。"""
        is_checked = self.ui.radioButton_snapshot.isChecked()
        if is_checked:
            if not self._snapshotPath:
                # 尝试从comboBox_snapshot获取快照路径
                index = self.ui.comboBox_snapshot.currentIndex()
                self._snapshotPath = self.ui.comboBox_snapshot.itemData(index, Qt.UserRole)
                if not self._snapshotPath:
                    # 如果仍然没有快照路径，提示创建
                    branch = self.ui.comboBox_allBranches.currentText()
                    platform = self.ui.comboBox_platform.currentText()
                    self.promptCreateSnapshot(branch, platform)
        else:
            # 当取消勾选时，不需要将self._snapshotPath设置为None
            pass
        self.syncSnapshotCfg()

    def promptCreateSnapshot(self, branch, platform):
        """在没有快照时提示用户创建快照。"""
        reply = QMessageBox.question(
            self,
            "确认操作",
            "快照路径未设置，是否自动创建快照？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            XAUrl = KBMgr.getBranchUrl(branch)
            resUrl = FolderUtil.join(XAUrl, "res")
            filesDict = FolderUtil.getFilesInfo(resUrl)
            if not filesDict:
                QMessageBox.warning(self, "目标资源不存在", "请检查目标资源路径是否正确。")
                self.ui.radioButton_snapshot.setChecked(False)
                self._snapshotPath = None
                return
            file_md5_map = Md5Util.fileTreeSnapshot(filesDict)
            snapshot_environment = JsonUtil.readInCfg('environment').get('snapshot')
            branch_platform = f'{branch}_{platform}'
            snapshot_cfg_path = FolderUtil.join(snapshot_environment, branch_platform)
            if not FolderUtil.exists(snapshot_cfg_path):
                FolderUtil.create(snapshot_cfg_path)
            unique_id = self._uniqueKey.split('-')[1]
            new_snapshot_cfg_path = f'{snapshot_cfg_path}/snapshot_{unique_id}.json'
            JsonUtil.writeDict(file_md5_map, new_snapshot_cfg_path)

            # 更新binding_info和snapshot_binding
            snapshot_binding = JsonUtil.readInCfg('snapshot_binding') or {}
            binding_info = snapshot_binding.get(branch) or {}
            binding_info[f'snapshot_{platform}'] = new_snapshot_cfg_path
            snapshot_binding[branch] = binding_info
            JsonUtil.saveInCfg('snapshot_binding', snapshot_binding)

            self._snapshotPath = new_snapshot_cfg_path
            self.displaySnapshot()
        else:
            self.ui.radioButton_snapshot.setChecked(False)
            self._snapshotPath = None

    def refreshQuicParasComboBox(self):
        """刷新快速参数组合框。"""
        self.ui.comboBox_quicParas.clear()
        all_paras = JsonUtil.read(JsonUtil.PARAS)
        self.ui.comboBox_quicParas.addItems(all_paras.keys())
        if not all_paras:
            self.setBuildView({})
            self.setBuildDefault()

    def onQuicParasAddAccepted(self, name):
        """当添加快速参数后回调。"""
        self.refreshQuicParasComboBox()
        self.ui.comboBox_quicParas.setCurrentText(name)

    def onClickQuicParasAdd(self):
        """处理添加快速参数的点击事件。"""
        self.ui.TipsDialog = QuicParasAddTips(self.onQuicParasAddAccepted)
        self.ui.TipsDialog.show()

    def onParasBoxChanged(self):
        """处理快速参数选择的变化。"""
        name = self.ui.comboBox_quicParas.currentText()
        if not name:
            return
        para_vo = JsonUtil.readIn(JsonUtil.PARAS, name)
        self.setBuildView(para_vo)

    def onClickQuicParasSync(self, force=False):
        """同步快速参数。"""
        name = self.ui.comboBox_quicParas.currentText()
        if name in ['and_hwzs', 'and_ajmzs', 'and_hwzs64', 'ios_ajmzs', 'ios_hwzs', 'mclient']:
            if not AuthManager.is_admin_authenticated() and not force:
                QMessageBox.warning(self, "同步失败", "线上方案不能修改。")
                return

        if not name:
            QMessageBox.warning(self, "同步失败", "请先添加一条快速参数。")

        else:
            para_dict = self.getBuildDict()
            self.paraVo = ToolsMain.inputByDict(para_dict)
            JsonUtil.saveIn(JsonUtil.PARAS, name, self.paraVo.getAll())
            if not force:
                QMessageBox.information(self, "同步成功", "快速参数同步成功。")

    def onClickQuicParasDel(self):
        """处理删除快速参数的点击事件。"""
        name = self.ui.comboBox_quicParas.currentText()
        JsonUtil.deleteIn(JsonUtil.PARAS, name)
        self.refreshQuicParasComboBox()

    def onComboBoxChanged(self):
        """处理分支或平台选择的变化。"""
        self.ui.lineEdit_pathSet.clear()
        branch = self.ui.comboBox_allBranches.currentText()
        path = KBMgr.getBranchUrl(branch)
        if path:
            self.ui.lineEdit_pathSet.setText(path)
        self.displaySnapshot()

    def displaySnapshot(self):
        """根据当前分支和平台显示快照信息。"""
        branch = self.ui.comboBox_allBranches.currentText()
        platform = self.ui.comboBox_platform.currentText()
        snapshot_binding = JsonUtil.readInCfg('snapshot_binding') or {}
        binding_info = snapshot_binding.get(branch)
        if binding_info:
            self.ui.radioButton_snapshot.setChecked(binding_info.get('check', False))
            self._snapshotPath = binding_info.get(f'snapshot_{platform}', '')
            self.ui.comboBox_snapshot.clear()
            snapshot_environment = JsonUtil.readInCfg('environment').get('snapshot')
            branch_platform = f'{branch}_{platform}'
            snapshot_cfg_path = FolderUtil.join(snapshot_environment, branch_platform)
            snapshot_cfgs = FolderUtil.getFilesInfo(snapshot_cfg_path)
            snapshot_cfgs_sorted = sorted(
                snapshot_cfgs.items(),
                key=lambda x: FolderUtil.getLastModifiedTime(x[1]),
                reverse=True
            )
            snapshot_file_paths = [file_path for _, file_path in snapshot_cfgs_sorted]

            # 添加项时，设置右对齐，并添加工具提示
            for file_path in snapshot_file_paths:
                file_name = os.path.basename(file_path)
                self.ui.comboBox_snapshot.addItem(file_name)
                index = self.ui.comboBox_snapshot.findText(file_name)
                self.ui.comboBox_snapshot.setItemData(index, file_path, Qt.ToolTipRole)  # 工具提示
                self.ui.comboBox_snapshot.setItemData(index, file_path, Qt.UserRole)     # 用户数据，存储完整路径
                self.ui.comboBox_snapshot.setItemData(index, Qt.AlignRight, Qt.TextAlignmentRole)

            # 设置comboBox_snapshot的当前选择
            if self._snapshotPath and self._snapshotPath in snapshot_file_paths:
                index = snapshot_file_paths.index(self._snapshotPath)
                self.ui.comboBox_snapshot.setCurrentIndex(index)
            elif snapshot_file_paths:
                self.ui.comboBox_snapshot.setCurrentIndex(0)
                # 更新self._snapshotPath
                index = self.ui.comboBox_snapshot.currentIndex()
                self._snapshotPath = self.ui.comboBox_snapshot.itemData(index, Qt.UserRole)

        else:
            self.ui.radioButton_snapshot.setChecked(False)
            self.ui.comboBox_snapshot.clear()
            self._snapshotPath = None

    def onClickPathSet(self):
        """处理设置工程路径的点击事件。"""
        path = InputUtil.InPutDirectoryGUI()
        if not path:
            return
        self.ui.lineEdit_pathSet.setText(path)
        branch = self.ui.comboBox_allBranches.currentText()
        KBMgr.setBranchUrl(branch, path)

    def onPathSet(self):
        """当工程路径文本变化时更新路径。"""
        path = self.ui.lineEdit_pathSet.text()
        if not path:
            return
        branch = self.ui.comboBox_allBranches.currentText()
        KBMgr.setBranchUrl(branch, path)

    def setBuildDefault(self):
        """设置默认的构建参数。"""
        all_paras = JsonUtil.read(JsonUtil.PARAS)
        if all_paras:
            return
        self.ui.lineEdit_bigversion.setPlaceholderText(FOA_BUILD_VO['bigversion'])
        self.ui.lineEdit_channel.setPlaceholderText(FOA_BUILD_VO['channel'])
        self.ui.lineEdit_foaName.setPlaceholderText(FOA_BUILD_VO['foaName'])
        self.ui.lineEdit_focName.setPlaceholderText(FOA_BUILD_VO['focName'])
        self.ui.lineEdit_sysversion.setPlaceholderText(FOA_BUILD_VO['sysversion'])
        self.ui.lineEdit_targetRes.setPlaceholderText(FOA_BUILD_VO['res_target'])

        # 设置组合框的默认选择
        self.ui.comboBox_isDebug.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['isdebug']))
        self.ui.comboBox_sandBox.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['sandbox']))
        self.ui.comboBox_useLocals.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['use_localserverlist']))
        self.ui.comboBox_useSDK.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['use_sdk']))
        self.ui.comboBox_testapp.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['istestapp']))
        self.ui.comboBox_appstore.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['isAppleStoreReview']))
        self.ui.comboBox_lang.setCurrentText(FOA_BUILD_VO['lang'])
        self.ui.comboBox_platform.setCurrentText(FOA_BUILD_VO['platform'])
        self.ui.comboBox_is64.setCurrentText(StringUtil.Py2LuaBool(FOA_BUILD_VO['is64']))

    def setBuildView(self, buildDict):
        """从字典中设置构建参数。"""
        self.ui.lineEdit_bigversion.setText(buildDict.get('bigversion', ''))
        self.ui.lineEdit_channel.setText(buildDict.get('channel', ''))
        self.ui.lineEdit_foaName.setText(buildDict.get('foaName', ''))
        self.ui.lineEdit_focName.setText(buildDict.get('focName', ''))
        self.ui.lineEdit_sysversion.setText(buildDict.get('sysversion', ''))
        self.ui.lineEdit_targetRes.setText(buildDict.get('res_target', ''))

        # 更新组合框
        self.ui.comboBox_isDebug.setCurrentText(StringUtil.Py2LuaBool(buildDict.get('isdebug', FOA_BUILD_VO['isdebug'])))
        self.ui.comboBox_sandBox.setCurrentText(StringUtil.Py2LuaBool(buildDict.get('sandbox', FOA_BUILD_VO['sandbox'])))
        self.ui.comboBox_useLocals.setCurrentText(StringUtil.Py2LuaBool(buildDict.get('use_localserverlist', FOA_BUILD_VO['use_localserverlist'])))
        self.ui.comboBox_useSDK.setCurrentText(StringUtil.Py2LuaBool(buildDict.get('use_sdk', FOA_BUILD_VO['use_sdk'])))
        self.ui.comboBox_testapp.setCurrentText(StringUtil.Py2LuaBool(buildDict.get('istestapp', FOA_BUILD_VO['istestapp'])))
        self.ui.comboBox_appstore.setCurrentText(StringUtil.Py2LuaBool(buildDict.get('isAppleStoreReview', FOA_BUILD_VO['isAppleStoreReview'])))
        self.ui.comboBox_lang.setCurrentText(buildDict.get('lang', FOA_BUILD_VO['lang']))
        self.ui.comboBox_platform.setCurrentText(buildDict.get('platform', FOA_BUILD_VO['platform']))
        self.ui.comboBox_is64.setCurrentText(StringUtil.Py2LuaBool(buildDict.get('is64', FOA_BUILD_VO['is64'])))

        self.ui.lineEdit_outPath1.setText(buildDict.get('outPath1', ''))
        self.ui.lineEdit_outPath2.setText(buildDict.get('outPath2', ''))

    def getBuildDict(self):
        """从UI收集构建参数到字典中。"""
        buildDict = {
            'opt': self._uniqueKey.split('-')[0],
            'bigversion': self.ui.lineEdit_bigversion.text(),
            'branches': self.ui.comboBox_allBranches.currentText(),
            'channel': self.ui.lineEdit_channel.text(),
            'foaName': self.ui.lineEdit_foaName.text(),
            'focName': self.ui.lineEdit_focName.text(),
            'sysversion': self.ui.lineEdit_sysversion.text(),
            'tag': self.ui.lineEdit_channel.text(),
            'res_target': self.ui.lineEdit_targetRes.text() or None,
            'snapshotPath': self._snapshotPath,
            'outPath1': self.ui.lineEdit_outPath1.text(),
            'outPath2': self.ui.lineEdit_outPath2.text(),
            'isdebug': StringUtil.Lua2PyBool(self.ui.comboBox_isDebug.currentText()),
            'sandbox': StringUtil.Lua2PyBool(self.ui.comboBox_sandBox.currentText()),
            'use_localserverlist': StringUtil.Lua2PyBool(self.ui.comboBox_useLocals.currentText()),
            'use_sdk': StringUtil.Lua2PyBool(self.ui.comboBox_useSDK.currentText()),
            'istestapp': StringUtil.Lua2PyBool(self.ui.comboBox_testapp.currentText()),
            'isAppleStoreReview': StringUtil.Lua2PyBool(self.ui.comboBox_appstore.currentText()),
            'lang': self.ui.comboBox_lang.currentText(),
            'platform': self.ui.comboBox_platform.currentText(),
            'is64': StringUtil.Lua2PyBool(self.ui.comboBox_is64.currentText())
        }
        return buildDict

    def getFuncOutPath(self):
        """根据唯一键生成功能输出路径。"""
        foa_build_path = 'sample/output/'
        arr = self._uniqueKey.split('-', 1)
        work_dir = f'{foa_build_path}/{arr[0]}/{arr[1]}/'
        if not FolderUtil.exists(work_dir):
            FolderUtil.create(work_dir)
        return work_dir

    def getVO(self):
        """获取参数VO（值对象）。"""
        return self.paraVo

    def addSysversion(self, sysversion):
        """自动递增系统版本号。"""
        if sysversion:
            version_parts = sysversion.split('.')
            if len(version_parts) == 3:
                version_parts[2] = str(int(version_parts[2]) + 1)
                new_sysversion = '.'.join(version_parts)
                self.ui.lineEdit_sysversion.setText(new_sysversion)
                LogMgr.getLogger(self._uniqueKey).info(f"自动递增版本号成功，新版本号：{new_sysversion}")
                self.onClickQuicParasSync(force=True)
            else:
                print("sysversion格式不正确")
        else:
            print("未找到系统版本信息")

    def onClickBuild(self):
        """处理构建按钮的点击事件。"""
        if self.ui.radioButton_batchBuild.isChecked():
            # 批量构建模式
            if not self.batchBuildDialog:
                QMessageBox.warning(self, "批量构建", "没有选中的配置进行批量构建。")
                return
            selected_configs = self.batchBuildDialog.getSelectedConfigurations()
            if not selected_configs:
                QMessageBox.warning(self, "批量构建", "没有选中的配置进行批量构建。")
                return
            self.is_batch_building = True
            build_results = []
            for config_name in selected_configs:
                index = self.ui.comboBox_quicParas.findText(config_name)
                if index != -1:
                    self.ui.comboBox_quicParas.setCurrentIndex(index)
                    self.onParasBoxChanged()  # 更新界面参数
                    success = self.performBuild()  # 执行构建逻辑
                    build_results.append((config_name, success))
                    if not success:
                        # 如果构建失败，停止批量构建
                        LogMgr.getLogger(self._uniqueKey).warning(f"构建失败，停止批量构建。配置：{config_name}")
                        QMessageBox.warning(self, "批量构建中断", f"构建失败，批量构建已中断。配置：{config_name}")
                        break
                else:
                    LogMgr.getLogger(self._uniqueKey).warning(f"未找到配置：{config_name}")
            self.is_batch_building = False
            # 构建结果摘要
            summary = "\n".join(
                [f"{name}: {'成功' if success else '失败'}" for name, success in build_results]
            )
            QMessageBox.information(self, "批量构建完成", f"批量构建已完成：\n{summary}")
        else:
            # 单个构建模式
            self.is_batch_building = False
            self.performBuild()

    def performBuild(self):
        """执行构建逻辑。"""
        paraDict = self.getBuildDict()
        self.logger.info('开始获取构建参数')
        self.paraVo = ToolsMain.inputByDict(paraDict)
        self.paraVo.setUniqueKey(self._uniqueKey)
        self.paraVo.setFuncOutPath(self.getFuncOutPath())

        # 校验
        branches = self.paraVo.getVal("branches")
        XA_Url = G.getG("KBMgr").getBranchUrl(branches)
        res_target = self.paraVo.getVal("res_target")
        platformRes = f'{XA_Url}/{res_target}'
        if not FolderUtil.exists(platformRes):
            error_message = (
                f"分支'{branches}'的工程路径中，没有文件夹'{res_target}'。\n"
                "请修改参数面板中目标资源或检查工程路径中的指定文件夹。"
            )
            self.logger.warning("目标资源不存在")
            if self.is_batch_building:
                # 在批量构建模式下，返回 False 表示失败
                return False
            else:
                QMessageBox.warning(self, "目标资源不存在", error_message)
                return

        snapshot_path = self.paraVo.getVal("snapshotPath")
        if snapshot_path and not FolderUtil.exists(snapshot_path):
            self.ui.radioButton_snapshot.setChecked(False)
            self._snapshotPath = None
            self.logger.warning(
                f'快照文件不存在，此次构建取消自动化转资源：{snapshot_path}')

        foa_errors, successed = ToolsMain.main(self.paraVo)
        if not foa_errors and successed:
            self.addSysversion(self.paraVo.getVal('sysversion'))
            self.syncSnapshotCfg()
            self.logger.info("构建成功")
            if not self.is_batch_building:
                QMessageBox.information(self, "构建成功", "构建成功")
        else:
            error_msg = "构建失败，请检查日志以获取详细信息。"
            self.logger.warning("构建失败")
            if self.is_batch_building:
                # 在批量构建模式下，返回 False 表示失败
                return False
            else:
                QMessageBox.warning(self, "构建失败", error_msg)
                return

        self.displaySnapshot()
        if self._callback:
            self._callback(self._uniqueKey)

        # 返回 True 表示成功
        return True

    def onSnapshotItemRightClicked(self, position):
        """处理快照下拉列表项的右键点击事件。"""
        index = self.ui.comboBox_snapshot.view().indexAt(position)
        if not index.isValid():
            return
        # 获取用户数据中的完整文件路径
        file_path = self.ui.comboBox_snapshot.itemData(index.row(), Qt.UserRole)
        if not file_path:
            return
        menu = QMenu()
        action_open_in_explorer = QAction("在文件资源管理器中显示", self)
        action_open_in_explorer.triggered.connect(lambda: TerminalUtil.open_in_explorer(file_path))
        menu.addAction(action_open_in_explorer)
        menu.exec_(QCursor.pos())
