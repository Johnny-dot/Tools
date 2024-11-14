import os
import subprocess
from PySide6.QtWidgets import QWidget, QListWidgetItem, QMenu, QMessageBox, QAbstractItemView
from PySide6.QtCore import Qt
from sample.qt.src.widget.ui_DetectDuplicateFilesWidget import Ui_DetectDuplicateFilesWidget
import sample.src_references.common.g.G as G
import sample.src_references.common.utils.InputUtil as InputUtil
import sample.src_references.Main as ToolsMain  # 导入Main模块
from sample.src_references.common.utils import FolderUtil, TerminalUtil


class DetectDuplicateFilesWidget(QWidget):
    def __init__(self, uniqueKey, callback):
        super().__init__(parent=None)
        self._callback = callback
        self._inPath = None
        self._uniqueKey = uniqueKey
        self._pendingResources = {}  # 初始化 _pendingResources 属性
        self.paraVo = None
        self.ui = Ui_DetectDuplicateFilesWidget()
        self.ui.setupUi(self)
        self.initDetectDuplicateFilesUI()
        G.getG('LogMgr').getLogger(self._uniqueKey).info(uniqueKey)

    def getUniqueKey(self):
        return self._uniqueKey

    def initDetectDuplicateFilesUI(self):
        self.ui.listWidget_pending.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置为单选
        self.ui.pushButton_build.clicked[bool].connect(self.onClickBuild)
        self.ui.toolButton_inPath.clicked[bool].connect(self.onClickInPath)
        self.ui.lineEdit_inPath.textChanged.connect(self.onSetInPath)
        self.ui.listWidget_pending.itemClicked.connect(self.showDuplicates)
        self.ui.listWidget_processed.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listWidget_processed.customContextMenuRequested.connect(self.showContextMenu)

    def onClickInPath(self):
        inPath = InputUtil.InPutDirectoryGUI()
        if inPath == "":
            return
        self.ui.lineEdit_inPath.setText(inPath)

    def onSetInPath(self, path):
        if FolderUtil.exists(path):
            if path and self._inPath != path:
                self._inPath = path
            G.getG('LogMgr').getLogger(self._uniqueKey).info("成功设置输入路径:%s" % self._inPath)
        else:
            G.getG('LogMgr').getLogger(self._uniqueKey).warning("路径不存在:%s" % path)

    def clearPendingList(self):
        self.ui.listWidget_pending.clear()
        self.ui.listWidget_processed.clear()
        self._pendingResources = {}  # 清空 _pendingResources

    def showDuplicates(self, item):
        md5 = item.data(Qt.UserRole)
        duplicate_info = self._pendingResources.get(md5, {})
        if not duplicate_info:
            return

        duplicates = duplicate_info['paths']
        size = duplicate_info['size']

        self.ui.listWidget_processed.clear()
        for file_path in duplicates:
            processed_item = QListWidgetItem(file_path)
            processed_item.setToolTip(f"MD5: {md5}\nPath: {file_path}\nSize: {self.convert_size(size)}")
            processed_item.setData(Qt.UserRole, file_path)
            self.ui.listWidget_processed.addItem(processed_item)

        # Optional: Update the total duplicates count and size somewhere in the UI
        duplicate_groups = len(duplicates)
        total_size = size * len(duplicates)
        G.getG('LogMgr').getLogger(self.getUniqueKey()).info(
            f"Detected {duplicate_groups} duplicate groups with a total size of {self.convert_size(total_size)}."
        )

    def showContextMenu(self, position):
        menu = QMenu()
        delete_action = menu.addAction("删除")
        open_action = menu.addAction("在资源管理器中打开")
        action = menu.exec_(self.ui.listWidget_processed.mapToGlobal(position))

        if action == delete_action:
            current_item = self.ui.listWidget_processed.currentItem()
            if current_item:
                file_path = current_item.data(Qt.UserRole)
                success, message = self.deleteFile(file_path)
                if success:
                    self.updateAfterDelete(file_path)
                    QMessageBox.information(self, "删除文件", message)
                else:
                    QMessageBox.warning(self, "删除文件", message)

        elif action == open_action:
            current_item = self.ui.listWidget_processed.currentItem()
            if current_item:
                file_path = current_item.data(Qt.UserRole)
                success, message = TerminalUtil.open_in_explorer(file_path)
                if not success:
                    QMessageBox.warning(self, "打开文件", message)

    def deleteFile(self, file_path):
        try:
            os.remove(file_path)  # 使用 os 模块删除文件
            return True, f"成功删除文件: {file_path}"
        except Exception as e:
            return False, f"删除文件失败: {str(e)}"

    def updateAfterDelete(self, file_path):
        md5 = None
        for md5_key, paths in self._pendingResources.items():
            if file_path in paths:
                paths.remove(file_path)
                md5 = md5_key
                break

        if md5 and not self._pendingResources[md5]:
            del self._pendingResources[md5]
            self.removeItemFromPending(md5)

        self.removeItemFromProcessed(file_path)

    def removeItemFromPending(self, md5):
        for i in range(self.ui.listWidget_pending.count()):
            item = self.ui.listWidget_pending.item(i)
            if item.data(Qt.UserRole) == md5:
                self.ui.listWidget_pending.takeItem(i)
                break

    def removeItemFromProcessed(self, file_path):
        for i in range(self.ui.listWidget_processed.count()):
            item = self.ui.listWidget_processed.item(i)
            if item.data(Qt.UserRole) == file_path:
                self.ui.listWidget_processed.takeItem(i)
                break

    def getBuildDict(self):
        opt = self._uniqueKey.split('-')[0]  # 根据uniqueKey动态生成opt

        buildDict = {
            'opt': opt,
            'inputUrl': self.ui.lineEdit_inPath.displayText(),
            'pendingResources': self._pendingResources,
            'match_text': self.ui.lineEdit_match.displayText(),
        }
        return buildDict

    def convert_size(self, size_bytes):
        """
        将字节转换为MB或GB的单位，按照Windows文件管理系统的显示规则。
        """
        if size_bytes < 1024:
            return f"{size_bytes} Bytes"
        elif size_bytes < 1024 ** 2:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 ** 3:
            return f"{size_bytes / 1024 ** 2:.2f} MB"
        else:
            return f"{size_bytes / 1024 ** 3:.2f} GB"

    def getFuncOutPath(self):
        FOA_BUILD_PATH = 'sample/output/'
        arr = self.getUniqueKey().split('-', 1)
        workDir = '%s/%s/%s/' % (FOA_BUILD_PATH, arr[0], arr[1])
        if not FolderUtil.exists(workDir):
            FolderUtil.create(workDir)
        return workDir

    def onClickBuild(self):
        if not self._inPath:
            QMessageBox.warning(self, "路径未设置", "请先设置路径后再进行检测。")
            return

        G.getG('LogMgr').getLogger(self._uniqueKey).info("开始检查重复文件...")

        buildDict = self.getBuildDict()
        self.paraVo = ToolsMain.inputByDict(buildDict)
        self.paraVo.setUniqueKey(self.getUniqueKey())
        self.paraVo.setFuncOutPath(self.getFuncOutPath())
        duplicates, duplicate_groups, total_size = ToolsMain.main(self.paraVo)  # 获取重复文件及统计信息

        self.ui.listWidget_pending.clear()
        if duplicates:
            self._pendingResources = duplicates  # 更新 _pendingResources 以供后续使用
            for md5, info in duplicates.items():
                item = QListWidgetItem(os.path.basename(info['paths'][0]))
                item.setData(Qt.UserRole, md5)
                self.ui.listWidget_pending.addItem(item)

            # 记录检测到的重复文件组数和总大小
            G.getG('LogMgr').getLogger(self._uniqueKey).info(
                f"检测到 {duplicate_groups} 组重复文件，总大小为 {self.convert_size(total_size)}。"
            )
        else:
            G.getG('LogMgr').getLogger(self._uniqueKey).info("未检测到重复文件。")
            QMessageBox.information(self, "检测完成", "未检测到重复文件。")

        if self._callback:
            self._callback(self.getUniqueKey())

