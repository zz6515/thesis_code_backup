import sys, time,os
from PyQt5 import QtCore,QtWidgets
from GUI.GUI_size import Ui_Size
from PyQt5.QtWidgets import QWidget, QPushButton,QApplication
class size(QWidget,Ui_Size):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def returnsize(self):
        QApplication.processEvents()
        return int(self.value.text())