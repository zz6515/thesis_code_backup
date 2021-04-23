# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_SFC.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 180)
        Form.setMinimumSize(QtCore.QSize(300, 180))
        Form.setMaximumSize(QtCore.QSize(300, 180))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_SFC = QtWidgets.QPushButton(Form)
        self.btn_SFC.setObjectName("btn_SFC")
        self.gridLayout.addWidget(self.btn_SFC, 5, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.blue = QtWidgets.QComboBox(Form)
        self.blue.setObjectName("blue")
        self.gridLayout_2.addWidget(self.blue, 4, 2, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(60, 0))
        self.label.setMaximumSize(QtCore.QSize(60, 20))
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setMinimumSize(QtCore.QSize(60, 0))
        self.label_3.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 4, 0, 1, 1)
        self.red = QtWidgets.QComboBox(Form)
        self.red.setObjectName("red")
        self.gridLayout_2.addWidget(self.red, 2, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 2, 1, 1)
        self.green = QtWidgets.QComboBox(Form)
        self.green.setObjectName("green")
        self.gridLayout_2.addWidget(self.green, 3, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setMinimumSize(QtCore.QSize(60, 0))
        self.label_2.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(60, 0))
        self.label_4.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "假彩色处理"))
        self.btn_SFC.setText(_translate("Form", "执行"))
        self.label.setText(_translate("Form", "红色"))
        self.label_3.setText(_translate("Form", "蓝色"))
        self.label_5.setText(_translate("Form", "Band"))
        self.label_2.setText(_translate("Form", "绿色"))
        self.label_4.setText(_translate("Form", "Channel"))
