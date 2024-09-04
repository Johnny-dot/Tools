# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QDialog

# Important:
# You need to run the following command to generate the ui_mainwindow.py file
#     pyside6-uic form.ui -o ui_mainwindow.py, or
#     pyside2-uic form.ui -o ui_mainwindow.py
from sample.qt.src.widget.ui_QuicParasAddTips import Ui_QuicParasAddTipsDialog

import sample.src_references.common.utils.JsonUtil as JsonUtil

class QuicParasAddTips(QDialog):
    def __init__(self, callback):
        super().__init__(parent=None)
        self.ui = Ui_QuicParasAddTipsDialog()
        self.ui.setupUi(self)
        self.callback = callback
        self.initTips()

    def initTips(self):
        self.ui.buttonBox.accepted.connect(self.onAccepted)
        self.ui.buttonBox.rejected.connect(self.onRejected)

    def onAccepted(self):
        name = self.ui.lineEdit_input.displayText()
        JsonUtil.saveIn(JsonUtil.PARAS, name, {})
        self.callback(name)

    def onRejected(self):
        print("reject")