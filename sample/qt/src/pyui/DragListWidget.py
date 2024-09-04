from PySide6 import QtCore, QtWidgets

class DragListWidget(QtWidgets.QListWidget):
    _signalDragEnterEvent = QtCore.Signal()
    _signalDragEvent = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(DragListWidget, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            self._signalDragEnterEvent.emit()
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        md = event.mimeData()
        if md.hasUrls():
            self._signalDragEvent.emit(md.urls())
            event.acceptProposedAction()