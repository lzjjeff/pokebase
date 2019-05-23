# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'child_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChildDialog(object):
    def setupUi(self, ChildDialog):
        ChildDialog.setObjectName("ChildDialog")
        ChildDialog.resize(462, 602)
        self.gridLayoutWidget = QtWidgets.QWidget(ChildDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 441, 521))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.from_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.from_label.setObjectName("from_label")
        self.gridLayout.addWidget(self.from_label, 1, 0, 1, 1)
        self.having_in = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.having_in.setObjectName("having_in")
        self.gridLayout.addWidget(self.having_in, 6, 1, 1, 1)
        self.groupby_in = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.groupby_in.setObjectName("groupby_in")
        self.gridLayout.addWidget(self.groupby_in, 5, 1, 1, 1)
        self.orderby_in = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.orderby_in.setObjectName("orderby_in")
        self.gridLayout.addWidget(self.orderby_in, 7, 1, 1, 1)
        self.select_in = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.select_in.setObjectName("select_in")
        self.gridLayout.addWidget(self.select_in, 0, 1, 1, 1)
        self.from_in = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.from_in.setObjectName("from_in")
        self.gridLayout.addWidget(self.from_in, 1, 1, 1, 1)
        self.where_in = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.where_in.setObjectName("where_in")
        self.gridLayout.addWidget(self.where_in, 3, 1, 1, 1)
        self.select_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.select_label.setObjectName("select_label")
        self.gridLayout.addWidget(self.select_label, 0, 0, 1, 1)
        self.orderby_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.orderby_label.setObjectName("orderby_label")
        self.gridLayout.addWidget(self.orderby_label, 7, 0, 1, 1)
        self.having_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.having_label.setObjectName("having_label")
        self.gridLayout.addWidget(self.having_label, 6, 0, 1, 1)
        self.groupby_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.groupby_label.setObjectName("groupby_label")
        self.gridLayout.addWidget(self.groupby_label, 5, 0, 1, 1)
        self.add_child_search_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.add_child_search_btn.setObjectName("add_child_search_btn")
        self.gridLayout.addWidget(self.add_child_search_btn, 4, 1, 1, 1)
        self.where_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.where_label.setObjectName("where_label")
        self.gridLayout.addWidget(self.where_label, 2, 0, 3, 1)
        self.cancel_btn = QtWidgets.QPushButton(ChildDialog)
        self.cancel_btn.setGeometry(QtCore.QRect(240, 540, 211, 51))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.cancel_btn.setFont(font)
        self.cancel_btn.setObjectName("cancel_btn")
        self.accept_btn = QtWidgets.QPushButton(ChildDialog)
        self.accept_btn.setGeometry(QtCore.QRect(10, 540, 211, 51))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.accept_btn.setFont(font)
        self.accept_btn.setObjectName("accept_btn")

        self.retranslateUi(ChildDialog)
        QtCore.QMetaObject.connectSlotsByName(ChildDialog)

    def retranslateUi(self, ChildDialog):
        _translate = QtCore.QCoreApplication.translate
        ChildDialog.setWindowTitle(_translate("ChildDialog", "Dialog"))
        self.from_label.setText(_translate("ChildDialog", "FROM"))
        self.select_label.setText(_translate("ChildDialog", "SELECT"))
        self.orderby_label.setText(_translate("ChildDialog", "ORDER BY"))
        self.having_label.setText(_translate("ChildDialog", "HAVING"))
        self.groupby_label.setText(_translate("ChildDialog", "GROUP BY"))
        self.add_child_search_btn.setText(_translate("ChildDialog", "添加子查询"))
        self.where_label.setText(_translate("ChildDialog", "WHERE"))
        self.cancel_btn.setText(_translate("ChildDialog", "取消"))
        self.accept_btn.setText(_translate("ChildDialog", "确认"))


