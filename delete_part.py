from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import Qt
class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(QtCore.QRectF(-500, -500, 1000, 1000), parent)
        self._start = QtCore.QPointF()
        self._current_rect_item = None
        self.size = 50
        self.brush = QBrush(Qt.SolidPattern)
        self.brush.setStyle(Qt.Dense6Pattern)
    def mousePressEvent(self, event):
        if self.itemAt(event.scenePos(), QtGui.QTransform()) is None:
            self._current_rect_item = QtWidgets.QGraphicsRectItem()
            self._current_rect_item.setBrush(self.brush)
            self._current_rect_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
            self.addItem(self._current_rect_item)
            r = QtCore.QRectF(event.scenePos().x()-int(self.size)/2,event.scenePos().y()-int(self.size)/2,self.size,self.size)
            self._current_rect_item.setRect(r)
        self.update()
        super(GraphicsScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._current_rect_item is not None:
            r = QtCore.QRectF(event.scenePos().x(),event.scenePos().y(),self.size,self.size).normalized()
            self._current_rect_item.setRect(r)
        self.update()
        super(GraphicsScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._current_rect_item = None
        super(GraphicsScene, self).mouseReleaseEvent(event)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        scene =GraphicsScene(self)
        view = QtWidgets.QGraphicsView(scene)
        self.setCentralWidget(view)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())