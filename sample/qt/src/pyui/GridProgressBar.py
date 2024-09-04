import sys
from PySide6.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor


class GridProgressBar(QWidget):
    def __init__(self, parent=None, rows=10, columns=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows = rows
        self.columns = columns
        self.total_blocks = self.rows * self.columns
        self.current_progress = 0
        self.initUI()

    def initUI(self):
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(1)  # Set space between blocks

        self.blocks = []

        for i in range(self.rows):
            row_blocks = []
            for j in range(self.columns):
                label = QLabel(self)
                label.setFixedSize(20, 20)  # Set block size
                label.setAutoFillBackground(True)

                palette = label.palette()
                palette.setColor(QPalette.Window, Qt.gray)
                label.setPalette(palette)

                self.grid_layout.addWidget(label, i, j)
                row_blocks.append(label)
            self.blocks.append(row_blocks)

    def update_progress(self, progress):
        # Calculate the number of blocks that should be green
        blocks_to_fill = int(self.total_blocks * (progress / 100.0))

        # Update blocks' color
        for i in range(self.total_blocks):
            row = i // self.columns
            col = i % self.columns
            label = self.blocks[row][col]

            palette = label.palette()
            if i < blocks_to_fill:
                palette.setColor(QPalette.Window, Qt.green)  # Filled block
            else:
                palette.setColor(QPalette.Window, Qt.gray)  # Unfilled block
            label.setPalette(palette)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = GridProgressBar()
#
#     window.show()
#
#     # Simulate progress update
#     for i in range(101):
#         window.update_progress(i)
#         QCoreApplication.processEvents()
#         time.sleep(0.05)  # Slow down the progress for demonstration
#
#     sys.exit(app.exec_())
