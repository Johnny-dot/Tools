import logging
from PySide6.QtGui import QColor, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import QTextEdit, QMessageBox, QApplication
from PySide6.QtCore import Qt, QTimer

class QTextEditLogger(logging.Handler):
    def __init__(self, textEditWidget: QTextEdit, parent=None):
        super().__init__()
        self.fuzzWord = None
        self.textEditWidget = textEditWidget
        self.textEditWidget.setReadOnly(True)
        self.parent = parent  # 需要一个父窗口来展示消息框
        self.error_message_position = None  # 记录最后一个错误消息框的位置
        self.error_messages = []  # 用于存储所有的QMessageBox实例

    def emit(self, record):
        msg = self.format(record)
        self.append_log_message(msg, record.levelno)

        # 如果是ERROR级别的日志，立即显示弹窗提示
        if record.levelno == logging.ERROR:
            self.show_error_message(msg)

    def append_log_message(self, msg, level):
        color = self.get_color_by_level(level)

        if not self.fuzzWord or self.fuzzWord == '':
            self.append_text(msg, color)
        elif self.fuzzWord in msg:
            self.append_text(msg, color)
        else:
            self.append_text(msg, color)

    def append_text(self, msg, color):
        cursor = self.textEditWidget.textCursor()
        cursor.movePosition(QTextCursor.End)

        format = QTextCharFormat()
        format.setForeground(QColor(color))

        cursor.insertText(msg + '\n', format)
        self.textEditWidget.setTextCursor(cursor)

    def setFuzzWord(self, word):
        self.fuzzWord = word

    def get_color_by_level(self, level):
        if level == logging.DEBUG:
            return "gray"
        elif level == logging.INFO:
            return "black"
        elif level == logging.WARNING:
            return "orange"
        elif level == logging.ERROR:
            return "red"
        elif level == logging.CRITICAL:
            return "darkred"
        else:
            return "black"

    def show_error_message(self, msg):
        # 创建QMessageBox，确保其父窗口为主窗口
        msg_box = QMessageBox(self.parent if self.parent else None)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText("An error has occurred")
        msg_box.setInformativeText(msg)
        msg_box.setWindowTitle("Error")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setWindowModality(Qt.NonModal)  # 设置为非模态
        msg_box.setWindowFlag(Qt.WindowStaysOnTopHint)  # 确保窗口总在最前

        # 如果有上一个错误消息框的位置，堆叠显示新框
        if self.error_message_position:
            x, y = self.error_message_position.x(), self.error_message_position.y()
            msg_box.move(x + 20, y + 20)  # 每个新框在 x 和 y 方向上错开20个像素
        else:
            screen_center = self.parent.geometry().center() if self.parent else msg_box.screen().geometry().center()
            msg_box.move(screen_center.x() - msg_box.width() // 2, screen_center.y() - msg_box.height() // 2)

        # 更新最后一个错误消息框的位置
        self.error_message_position = msg_box.pos()

        self.error_messages.append(msg_box)  # 将消息框保存到列表中

        msg_box.show()
        QApplication.processEvents()  # 立即处理事件循环，确保消息框立即显示
