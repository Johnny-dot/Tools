from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QCheckBox, QPushButton, QWidget, QHBoxLayout, QHeaderView
)
from PySide6.QtCore import Qt

# 导入 JsonUtil 模块
import sample.src_references.common.utils.JsonUtil as JsonUtil


class BatchBuildDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("批量构建配置")
        self.setModal(True)
        self.resize(400, 300)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["配置名称", "选择"])
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)  # 表头居中
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )  # 配置名称列自动伸展
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )  # 选择列根据内容调整宽度
        self.loadConfigurations()
        layout.addWidget(self.tableWidget)

        # 添加关闭按钮
        self.closeButton = QPushButton("关闭")
        self.closeButton.clicked.connect(self.onClose)
        layout.addWidget(self.closeButton)

        self.setLayout(layout)

    def loadConfigurations(self):
        # 读取保存的勾选状态
        saved_checked_configs = JsonUtil.readInCfg('batch_build_configs') or []

        all_paras = JsonUtil.read(JsonUtil.PARAS)
        configs = list(all_paras.keys())
        self.tableWidget.setRowCount(len(configs))
        for i, config_name in enumerate(configs):
            # 第一列：配置名称
            item = QTableWidgetItem(config_name)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tableWidget.setItem(i, 0, item)

            # 第二列：复选框
            checkbox = QCheckBox()
            checkbox.setChecked(config_name in saved_checked_configs)
            # 创建一个 QWidget 来容纳复选框，并使其居中
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignCenter)  # 居中
            layout.setContentsMargins(0, 0, 0, 0)
            self.tableWidget.setCellWidget(i, 1, widget)
            # 将复选框保存起来，以便后续获取状态
            checkbox.setProperty('config_name', config_name)

    def getSelectedConfigurations(self):
        selected_configs = []
        for row in range(self.tableWidget.rowCount()):
            # 获取复选框所在的 QWidget
            widget = self.tableWidget.cellWidget(row, 1)
            if widget is not None:
                checkbox = widget.findChild(QCheckBox)
                if checkbox.isChecked():
                    config_name = self.tableWidget.item(row, 0).text()
                    selected_configs.append(config_name)
        return selected_configs

    def onClose(self):
        # 保存勾选状态
        selected_configs = self.getSelectedConfigurations()
        JsonUtil.saveInCfg('batch_build_configs', selected_configs)
        self.close()
