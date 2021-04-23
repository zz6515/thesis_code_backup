import sys, time,os
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import Qt,QPoint, QPointF, QLine, QLineF, QRect, QRectF,QTime,qrand
from PyQt5.QtGui import QImage, QPixmap,QPainter,QBrush, QPen, QColor, QRadialGradient,QPainterPath,QPicture,QPolygonF,QPolygon
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QMessageBox, QFileDialog,QGraphicsScene, QGraphicsPixmapItem,QMainWindow,QGraphicsView,QGraphicsItem,QSizePolicy
#通过from…import…导入PyQt5中所需的模块，减轻脚本依赖。
from GUI.GUI_WindowMove import Ui_Form as WindowMove

class windowMove(QWidget,WindowMove):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def returnwidth(self):
        QApplication.processEvents()
        return int(self.lineEdit.text())
    def returnstep(self):
        QApplication.processEvents()
        return int(self.lineEdit_2.text())