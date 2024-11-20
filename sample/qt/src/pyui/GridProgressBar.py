from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import Qt

class GridProgressBar(QWidget):
    def __init__(self, parent=None, rows=10, columns=10, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.rows = rows
        self.columns = columns
        self.total_blocks = self.rows * self.columns
        self.current_progress = 0
        self.initUI()

    def initUI(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(1)  # 设置块之间的间距

        self.blocks = []

        for i in range(self.rows):
            row_blocks = []
            for j in range(self.columns):
                label = QLabel(self)
                label.setFixedSize(20, 20)  # 设置块大小

                # 使用样式表初始化块颜色为灰色
                label.setStyleSheet("background-color: gray;")

                self.grid_layout.addWidget(label, i, j)
                row_blocks.append(label)
            self.blocks.append(row_blocks)

    def update_progress(self, progress):
        # 计算应填充的绿色块数
        blocks_to_fill = int(self.total_blocks * (progress / 100.0))

        # 更新块的颜色
        for i in range(self.total_blocks):
            row = i // self.columns
            col = i % self.columns
            label = self.blocks[row][col]

            if i < blocks_to_fill:
                label.setStyleSheet("background-color: green;")  # 已填充的块
            else:
                label.setStyleSheet("background-color: gray;")   # 未填充的块
