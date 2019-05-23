# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1410, 895)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_label = QtWidgets.QLabel(self.centralwidget)
        self.main_label.setGeometry(QtCore.QRect(360, 230, 671, 161))
        font = QtGui.QFont()
        font.setPointSize(60)
        self.main_label.setFont(font)
        self.main_label.setObjectName("main_label")
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(580, 430, 191, 91))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.start_btn.setFont(font)
        self.start_btn.setObjectName("start_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1410, 26))
        self.menubar.setObjectName("menubar")
        self.database_menu = QtWidgets.QMenu(self.menubar)
        self.database_menu.setObjectName("database_menu")
        self.table_menu = QtWidgets.QMenu(self.menubar)
        self.table_menu.setObjectName("table_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.connect_action = QtWidgets.QAction(MainWindow)
        self.connect_action.setObjectName("connect_action")
        self.disconnect_action = QtWidgets.QAction(MainWindow)
        self.disconnect_action.setEnabled(False)
        self.disconnect_action.setObjectName("disconnect_action")
        self.add_action = QtWidgets.QAction(MainWindow)
        self.add_action.setEnabled(False)
        self.add_action.setObjectName("add_action")
        self.delete_action = QtWidgets.QAction(MainWindow)
        self.delete_action.setEnabled(False)
        self.delete_action.setObjectName("delete_action")
        self.database_menu.addAction(self.connect_action)
        self.database_menu.addAction(self.disconnect_action)
        self.table_menu.addAction(self.add_action)
        self.table_menu.addAction(self.delete_action)
        self.menubar.addAction(self.database_menu.menuAction())
        self.menubar.addAction(self.table_menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.main_label.setText(_translate("MainWindow", "Pokebase v0.1"))
        self.start_btn.setText(_translate("MainWindow", "开始"))
        self.database_menu.setTitle(_translate("MainWindow", "数据库"))
        self.table_menu.setTitle(_translate("MainWindow", "   表   "))
        self.connect_action.setText(_translate("MainWindow", "连接"))
        self.disconnect_action.setText(_translate("MainWindow", "断开"))
        self.add_action.setText(_translate("MainWindow", "添加"))
        self.delete_action.setText(_translate("MainWindow", "删除"))


