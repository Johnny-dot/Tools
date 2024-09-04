# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QWidget

# Important:
# You need to run the following command to generate the ui_mainwindow.py file
#     pyside6-uic form.ui -o ui_mainwindow.py, or
#     pyside2-uic form.ui -o ui_mainwindow.py
from sample.qt.src.widget.ui_BranchCoverWidget import Ui_BranchCoverWidget

import sample.src_references.common.g.G as G


class BranchCoverWidget(QWidget):
    def __init__(self, uniqueKey, callback):
        super().__init__(parent=None)
        self._callback = callback
        self.ui = Ui_BranchCoverWidget()
        self.ui.setupUi(self)
        self._uniqueKey = uniqueKey
        self.paraVo = None
        G.getG('LogMgr').getLogger(self._uniqueKey).info(uniqueKey)

    def getUniqueKey(self):
        return self._uniqueKey

    def getVO(self):
        return self.paraVo

    def onClickBuild(self):
        pass
        # paraDict = self.getBuildDict()
        # self.paraVo = ToolsMain.inputByDict(paraDict)
        # self.paraVo.setUniqueKey(self.getUniqueKey())
        # ToolsMain.main(self.paraVo)

        # if self._callback:
        #     self._callback()