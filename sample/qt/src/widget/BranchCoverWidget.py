# 该 Python 文件使用以下编码：utf-8
from datetime import datetime

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

# 重要：
# 您需要运行以下命令来生成 ui_mainwindow.py 文件
#     pyside6-uic form.ui -o ui_mainwindow.py，或者
#     pyside2-uic form.ui -o ui_mainwindow.py
from sample.qt.src.widget.ui_BranchCoverWidget import Ui_BranchCoverWidget

import sample.src_references.common.g.G as G
import sample.src_references.Main as ToolsMain
import sample.src_references.common.vos.BranchCoverVO as BranchCoverVO
from sample.src_references.common.utils import FolderUtil
from sample.src_references.common.vos.BranchCoverVO import OB_BRANCHES_REPO

MAIN_BRANCHES_REPO = BranchCoverVO.MAIN_BRANCHES_REPO
OB_BRANCHES_REPO = BranchCoverVO.OB_BRANCHES_REPO


class BranchCoverWidget(QWidget):
    def __init__(self, uniqueKey, callback):
        super().__init__(parent=None)
        self._callback = callback
        self.ui = Ui_BranchCoverWidget()
        self.ui.setupUi(self)
        self.initBranchCoverPage()
        self._uniqueKey = uniqueKey
        self.paraVo = None
        G.getG('LogMgr').getLogger(self._uniqueKey).info(uniqueKey)

    def getUniqueKey(self):
        return self._uniqueKey

    def getFuncOutPath(self):
        FOA_BUILD_PATH = 'sample/output/'
        arr = self.getUniqueKey().split('-', 1)
        workDir = '%s/%s/%s/' % (FOA_BUILD_PATH, arr[0], arr[1])
        if not FolderUtil.exists(workDir):
            FolderUtil.create(workDir)
        return workDir

    def getVO(self):
        return self.paraVo

    def initBranchCoverPage(self):
        # 连接构建按钮的点击事件
        self.ui.pushButton_build.clicked.connect(self.onClickBuild)

        # 设置主分支的 comboBox
        self.ui.comboBox_main.clear()
        for key, value in MAIN_BRANCHES_REPO.items():
            display_text = f"{key}: {value}"
            self.ui.comboBox_main.addItem(display_text, userData=value)
            index = self.ui.comboBox_main.count() - 1
            self.ui.comboBox_main.setItemData(index, display_text, Qt.ToolTipRole)  # 设置工具提示以显示完整文本

        # 设置 ob 分支的 comboBox
        self.ui.comboBox_ob.clear()
        for key, value in OB_BRANCHES_REPO.items():
            display_text = f"{key}: {value}"
            print(display_text, "OB_BRANCHES_REPO")
            self.ui.comboBox_ob.addItem(display_text, userData=value)
            index = self.ui.comboBox_ob.count() - 1
            self.ui.comboBox_ob.setItemData(index, display_text, Qt.ToolTipRole)  # 设置工具提示以显示完整文本

    from datetime import datetime

    def getBuildDict(self):
        # 获取源地址和目标地址
        source_repository_url = self.ui.comboBox_main.currentData()
        destination_repository_url = self.ui.comboBox_ob.currentData()

        # 获取构建字典，包含主分支和 ob 分支的数据
        commit_message = self.ui.textEdit_log.toPlainText()

        # 如果 commit_message 为空，使用当前日期、时间、源地址和目标地址作为默认提交信息
        if not commit_message.strip():
            commit_message = (
                f"自动提交于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
                f"源: {source_repository_url}, 目标: {destination_repository_url}"
            )

        buildDict = {
            "opt": "BRANCH_COVER",
            "source_repository_url": source_repository_url,
            "destination_repository_url": destination_repository_url,
            "commit_message": commit_message
        }
        return buildDict

    def onClickBuild(self):
        # 处理构建按钮点击事件
        paraDict = self.getBuildDict()
        self.paraVo = ToolsMain.inputByDict(paraDict)
        self.paraVo.setUniqueKey(self.getUniqueKey())
        self.paraVo.setFuncOutPath(self.getFuncOutPath())
        ToolsMain.main(self.paraVo)

        if self._callback:
            self._callback(self._uniqueKey)