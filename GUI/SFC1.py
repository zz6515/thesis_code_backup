import sys, time,os
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import Qt,QPoint, QPointF, QLine, QLineF, QRect, QRectF,QTime,qrand
from PyQt5.QtGui import QImage, QPixmap,QPainter,QBrush, QPen, QColor, QRadialGradient,QPainterPath,QPicture,QPolygonF,QPolygon
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QMessageBox, QFileDialog,QGraphicsScene, QGraphicsPixmapItem,QMainWindow,QGraphicsView,QGraphicsItem,QSizePolicy
#通过from…import…导入PyQt5中所需的模块，减轻脚本依赖。
from GUI.GUI_SFC import Ui_Form as SFC

class sFC(QWidget,SFC):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.count1 = 2
        self.count2 = 1
        self.count3 = 0
    def build_comboBox(self,count):
        for i in range (1,count+1):
            self.red.addItem(str(i))
            self.green.addItem(str(i))
            self.blue.addItem(str(i))