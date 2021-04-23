# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_size.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Size(object):
    def setupUi(self, Size):
        Size.setObjectName("Size")
        Size.resize(137, 73)
        self.verticalLayout = QtWidgets.QVBoxLayout(Size)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Size)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.value = QtWidgets.QLineEdit(Size)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.value.sizePolicy().hasHeightForWidth())
        self.value.setSizePolicy(sizePolicy)
        self.value.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.value.setObjectName("value")
        self.verticalLayout.addWidget(self.value, 0, QtCore.Qt.AlignHCenter)
        self.btn_Size = QtWidgets.QPushButton(Size)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_Size.sizePolicy().hasHeightForWidth())
        self.btn_Size.setSizePolicy(sizePolicy)
        self.btn_Size.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_Size.setObjectName("btn_Size")
        self.verticalLayout.addWidget(self.btn_Size, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

        self.retranslateUi(Size)
        QtCore.QMetaObject.connectSlotsByName(Size)

    def retranslateUi(self, Size):
        _translate = QtCore.QCoreApplication.translate
        Size.setWindowTitle(_translate("Size", "采样尺寸"))
        self.label.setText(_translate("Size", "请输入采样尺寸"))
        self.value.setText(_translate("Size", "800"))
        self.btn_Size.setText(_translate("Size", "确定"))
