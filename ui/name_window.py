# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'name_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NameDialog(object):
    def setupUi(self, NameDialog):
        NameDialog.setObjectName("NameDialog")
        NameDialog.resize(342, 130)
        NameDialog.setSizeGripEnabled(False)
        self.cancel_btn = QtWidgets.QPushButton(NameDialog)
        self.cancel_btn.setGeometry(QtCore.QRect(180, 70, 151, 41))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.cancel_btn.setFont(font)
        self.cancel_btn.setObjectName("cancel_btn")
        self.accept_btn = QtWidgets.QPushButton(NameDialog)
        self.accept_btn.setGeometry(QtCore.QRect(10, 70, 151, 41))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.accept_btn.setFont(font)
        self.accept_btn.setObjectName("accept_btn")
        self.nameEdit = QtWidgets.QLineEdit(NameDialog)
        self.nameEdit.setGeometry(QtCore.QRect(90, 20, 231, 41))
        self.nameEdit.setObjectName("nameEdit")
        self.nameLabel = QtWidgets.QLabel(NameDialog)
        self.nameLabel.setGeometry(QtCore.QRect(20, 20, 61, 41))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")

        self.retranslateUi(NameDialog)
        QtCore.QMetaObject.connectSlotsByName(NameDialog)

    def retranslateUi(self, NameDialog):
        _translate = QtCore.QCoreApplication.translate
        NameDialog.setWindowTitle(_translate("NameDialog", "Dialog"))
        self.cancel_btn.setText(_translate("NameDialog", "取消"))
        self.accept_btn.setText(_translate("NameDialog", "确认"))
        self.nameLabel.setText(_translate("NameDialog", "视图名"))


