import sys
import pymysql as mysql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from ui.start_window import *
from ui.child_window import *
from ui.name_window import *


class PokebaseApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(PokebaseApp, self).__init__(parent)
        self.setupUi(self)
        self.db = None
        self.is_connect = False
        self.opened_tables = {}
        self.start_btn.clicked.connect(self.start)

    def start(self):
        self._delete_parts()
        self._create_parts()

    def _delete_parts(self):
        self.main_label.deleteLater()
        self.start_btn.deleteLater()

    def _create_parts(self):
        self.error_label = QtWidgets.QLabel(self.centralwidget)
        self.error_label.setGeometry(QtCore.QRect(10, 820, 1381, 20))
        self.error_label.setText("")
        self.error_label.setObjectName("error_label")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setGeometry(QtCore.QRect(1120, 30, 281, 511))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 279, 509))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.scrollArea_3 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_3.setGeometry(QtCore.QRect(0, 0, 281, 811))
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 279, 809))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.pokebase_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.pokebase_label.setGeometry(QtCore.QRect(10, 0, 101, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.pokebase_label.setFont(font)
        self.pokebase_label.setObjectName("pokebase_label")
        self.table_list = QtWidgets.QListWidget(self.scrollAreaWidgetContents_3)
        self.table_list.setGeometry(QtCore.QRect(0, 30, 281, 781))
        self.table_list.setResizeMode(QtWidgets.QListView.Adjust)
        self.table_list.setObjectName("table_list")
        self.table_list.itemDoubleClicked.connect(self.open_table)  # 双击触发绑定的槽函数
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(300, 0, 801, 811))
        self.tabWidget.setIconSize(QtCore.QSize(20, 20))
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.tabCloseRequested.connect(self.close_table)   # 关闭信号
        self.scrollArea_4 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_4.setGeometry(QtCore.QRect(1120, 550, 281, 251))
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 279, 249))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.sql_text = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents_4)
        self.sql_text.setGeometry(QtCore.QRect(0, 30, 281, 221))
        self.sql_text.setObjectName("sql_text")
        self.sql_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.sql_label.setGeometry(QtCore.QRect(10, 0, 81, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.sql_label.setFont(font)
        self.sql_label.setObjectName("sql_label")
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)

        QtCore.QMetaObject.connectSlotsByName(self)

        self.pokebase_label.setText("Pokebase")
        self.sql_label.setText("SQL命令")

        # 设置响应事件
        self.connect_action.triggered.connect(self.connect)
        self.disconnect_action.triggered.connect(self.disconnect)
        self.add_action.triggered.connect(self.create_table)
        self.delete_action.triggered.connect(self.remove_table)

        self.error_label.show()
        self.scrollArea_2.show()
        self.scrollAreaWidgetContents_2.show()
        self.scrollArea_3.show()
        self.scrollAreaWidgetContents_3.show()
        self.pokebase_label.show()
        self.table_list.show()
        self.tabWidget.show()
        self.scrollArea_4.show()
        self.scrollAreaWidgetContents_4.show()
        self.sql_text.show()
        self.sql_label.show()

    def connect(self):
        self.db = mysql.connect("localhost", "lzjjeff", "lzj503167408", "pokebase")
        self.cursor = self.db.cursor()
        self.is_connect = True
        self.connect_action.setEnabled(False)
        self.disconnect_action.setEnabled(True)
        self.add_action.setEnabled(True)
        self.delete_action.setEnabled(True)
        tables = self.sql("show tables;")
        for table in tables:
            item = QtWidgets.QListWidgetItem()
            item.setText(table[0])
            self.table_list.addItem(item)
        # 初始化搜索界面
        self.init_search_ui()

    def disconnect(self):
        self.db.close()
        self.is_connect = False
        self.disconnect_action.setEnabled(False)
        self.add_action.setEnabled(False)
        self.delete_action.setEnabled(False)
        self.connect_action.setEnabled(True)

        # 清空列表
        self.table_list.clear()
        self.tabWidget.clear()

    def create_table(self):
        pass

    def remove_table(self):
        pass

    def open_table(self, item):
        if item.text() in self.opened_tables.keys():
            pass
        else:
            try:
                tuples = self.sql("select * from " + item.text() + ";")
                col_names = self.sql("desc " + item.text() + ";")
            except Exception as e:
                self.error_label.setText(str(e))
                return

            tab = QtWidgets.QWidget()
            tab.setObjectName(item.text())
            scrollArea = QtWidgets.QScrollArea(tab)
            scrollArea.setGeometry(QtCore.QRect(0, 30, 791, 741))
            scrollArea.setWidgetResizable(True)
            scrollArea.setObjectName("scrollArea")
            scrollAreaWidgetContents = QtWidgets.QWidget()
            scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 789, 739))
            scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
            # 创建表格
            table_info = QtWidgets.QTableWidget(scrollAreaWidgetContents)
            table_info.setGeometry(QtCore.QRect(0, 0, 791, 741))
            table_info.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            table_info.setObjectName("table_info")
            row_num = len(tuples)
            col_num = len(col_names)
            table_info.setColumnCount(col_num)
            table_info.setRowCount(row_num)
            col = 0
            for name in col_names:
                tw_item = QtWidgets.QTableWidgetItem(name[0])
                table_info.setHorizontalHeaderItem(col, tw_item)
                col += 1
            # 填充表格
            for i in range(len(tuples)):
                for j in range(len(col_names)):
                    t_item = QtWidgets.QTableWidgetItem(str(tuples[i][j]))
                    # t_item.setTextAlignment(Qt.AlignCenter)
                    table_info.setItem(i, j, t_item)
            table_info.sortByColumn(0, Qt.AscendingOrder)
            self.opened_tables[item.text()] = table_info

            scrollArea.setWidget(scrollAreaWidgetContents)
            add_btn = QtWidgets.QPushButton(tab)
            add_btn.setGeometry(QtCore.QRect(0, 0, 61, 31))
            add_btn.setObjectName("add_btn")
            add_btn.setText("添加")
            delete_btn = QtWidgets.QPushButton(tab)
            delete_btn.setGeometry(QtCore.QRect(60, 0, 61, 31))
            delete_btn.setObjectName("delete_btn")
            delete_btn.setText("删除")
            buttonBox = QtWidgets.QDialogButtonBox(tab)
            buttonBox.setEnabled(False)
            buttonBox.setGeometry(QtCore.QRect(590, 0, 193, 28))
            buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
            buttonBox.setObjectName("buttonBox")
            add_btn.clicked.connect(lambda: self.add_tuple(buttonBox))
            delete_btn.clicked.connect(lambda: self.delete_tuple(buttonBox))
            buttonBox.accepted.connect(lambda: self._accept(buttonBox))
            buttonBox.rejected.connect(lambda: self._reject(buttonBox))
            self.tabWidget.addTab(tab, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(tab), item.text())
            self.tabWidget.setCurrentWidget(tab)

    def close_table(self, item):
        if item == self.tabWidget.currentIndex():
            self.tabWidget.currentWidget().deleteLater()
            key = self.tabWidget.currentWidget().objectName()
            self.opened_tables.pop(key)

    def add_tuple(self, buttonBox):
        tab = self.tabWidget.currentWidget()
        table = self.opened_tables[tab.objectName()]
        row = table.rowCount()
        table.setRowCount(row+1)
        table.setCurrentCell(row, 0)
        buttonBox.setEnabled(True)

    def _accept(self, buttonBox):
        added_tuple = [[], []]
        tab = self.tabWidget.currentWidget()
        table = self.opened_tables[tab.objectName()]
        row = table.currentRow()
        try:
            for i in range(table.columnCount()):
                key = table.horizontalHeaderItem(i).text()
                value = table.item(row, i).text()
                added_tuple[0].append(key)
                added_tuple[1].append("\'" + value + "\'")
        except Exception as e:
            self.error_label.setText(str(e))
            buttonBox.setEnabled(False)
            return

        cmd = "insert into " + tab.objectName() + "(" + \
              ", ".join(added_tuple[0]) + ")\nvalues(" + \
              ", ".join(added_tuple[1]) + ");"
        try:
            self.sql(cmd)
        except Exception as e:
            self.error_label.setText(str(e))
            buttonBox.setEnabled(False)
            return
        buttonBox.setEnabled(False)

    def _reject(self, buttonBox):
        tab = self.tabWidget.currentWidget()
        table = self.opened_tables[tab.objectName()]
        table.removeRow(table.rowCount()-1)
        buttonBox.setEnabled(False)

    def delete_tuple(self, buttonBox):
        tab = self.tabWidget.currentWidget()
        table = self.opened_tables[tab.objectName()]
        current_row = table.currentRow()
        col_name = table.horizontalHeaderItem(0).text()
        value = table.item(current_row, 0).text()
        try:
            self.sql("delete from " + tab.objectName() + " where " +
                    col_name + " = " + value + ";")
        except Exception as e:
            self.error_label.setText(str(e))
            buttonBox.setEnabled(False)
            return
        table.removeRow(current_row)
        buttonBox.setEnabled(False)

    # search part
    def init_search_ui(self):
        self.searchTabWidget = QtWidgets.QTabWidget(self.scrollAreaWidgetContents_2)
        self.searchTabWidget.setGeometry(QtCore.QRect(0, 0, 281, 511))
        self.searchTabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.searchTabWidget.setObjectName("searchTabWidget")
        # 一般查询
        self._normal_search_ui()
        # 特殊查询
        self._special_search_ui()
        # 索引
        self._index_ui()

        self.searchTabWidget.show()

    def _normal_search_ui(self):
        self.search_tab = QtWidgets.QWidget()
        self.search_tab.setObjectName("search_tab")
        self.selectBox = QtWidgets.QComboBox(self.search_tab)
        self.selectBox.setGeometry(QtCore.QRect(90, 10, 171, 31))
        self.selectBox.setObjectName("selectBox")
        self.selectBox.addItem("pokedex")
        self.selectBox.addItem("pokemon")
        self.selectBox.addItem("pokemon_stats")
        self.selectBox.addItem("region")
        self.selectBox.addItem("type")
        self.selectBox.addItem("move")
        self.selectBox.addItem("pokemon_moves")
        self.selectBox.addItem("damage_class")
        self.selectBox.currentIndexChanged.connect(self._selection_change)
        self.select_label = QtWidgets.QLabel(self.search_tab)
        self.select_label.setGeometry(QtCore.QRect(10, 10, 71, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.select_label.setFont(font)
        self.select_label.setObjectName("select_label")
        self.select_label.setText("请选择表")
        self.searchTabWidget.addTab(self.search_tab, "查询")

        # pokemon
        self.pid = QtWidgets.QCheckBox(self.search_tab)
        self.pid.setGeometry(QtCore.QRect(20, 60, 61, 31))
        self.pid.setObjectName("pid")
        self.pid_in1 = QtWidgets.QLineEdit(self.search_tab)
        self.pid_in1.setGeometry(QtCore.QRect(100, 60, 71, 31))
        self.pid_in1.setObjectName("pid_in1")
        self.pid_in2 = QtWidgets.QLineEdit(self.search_tab)
        self.pid_in2.setGeometry(QtCore.QRect(190, 60, 71, 31))
        self.pid_in2.setObjectName("pid_in2")
        self._8 = QtWidgets.QLabel(self.search_tab)
        self._8.setGeometry(QtCore.QRect(180, 60, 16, 31))
        self._8.setObjectName("_8")
        self.pname = QtWidgets.QCheckBox(self.search_tab)
        self.pname.setGeometry(QtCore.QRect(20, 110, 71, 31))
        self.pname.setObjectName("pname")
        self.pname_in = QtWidgets.QComboBox(self.search_tab)
        self.pname_in.setGeometry(QtCore.QRect(100, 110, 161, 31))
        self.pname_in.setEditable(True)
        self.pname_in.setObjectName("pname_in")
        self.region = QtWidgets.QCheckBox(self.search_tab)
        self.region.setGeometry(QtCore.QRect(20, 160, 71, 31))
        self.region.setObjectName("region")
        self.region_in = QtWidgets.QComboBox(self.search_tab)
        self.region_in.setGeometry(QtCore.QRect(100, 160, 161, 31))
        self.region_in.setEditable(True)
        self.region_in.setObjectName("region_in")
        self.type1 = QtWidgets.QCheckBox(self.search_tab)
        self.type1.setGeometry(QtCore.QRect(20, 210, 71, 31))
        self.type1.setObjectName("type1")
        self.type1_in = QtWidgets.QComboBox(self.search_tab)
        self.type1_in.setGeometry(QtCore.QRect(100, 210, 161, 31))
        self.type1_in.setEditable(True)
        self.type1_in.setObjectName("type1_in")
        self.type2 = QtWidgets.QCheckBox(self.search_tab)
        self.type2.setGeometry(QtCore.QRect(20, 260, 71, 31))
        self.type2.setObjectName("type2")
        self.type2_in = QtWidgets.QComboBox(self.search_tab)
        self.type2_in.setGeometry(QtCore.QRect(100, 260, 161, 31))
        self.type2_in.setEditable(True)
        self.type2_in.setObjectName("type2_in")
        self.evolves_from = QtWidgets.QCheckBox(self.search_tab)
        self.evolves_from.setGeometry(QtCore.QRect(20, 310, 121, 31))
        self.evolves_from.setObjectName("evolves_from")
        self.evolves_from_in = QtWidgets.QComboBox(self.search_tab)
        self.evolves_from_in.setGeometry(QtCore.QRect(150, 310, 111, 31))
        self.evolves_from_in.setEditable(True)
        self.evolves_from_in.setObjectName("evolves_from_in")
        self.evolves_into = QtWidgets.QCheckBox(self.search_tab)
        self.evolves_into.setGeometry(QtCore.QRect(20, 360, 121, 31))
        self.evolves_into.setObjectName("evolves_into")
        self.evolves_into_in = QtWidgets.QComboBox(self.search_tab)
        self.evolves_into_in.setGeometry(QtCore.QRect(150, 360, 111, 31))
        self.evolves_into_in.setEditable(True)
        self.evolves_into_in.setObjectName("evolves_into_in")
        # pokemon_stats
        self.hp = QtWidgets.QCheckBox(self.search_tab)
        self.hp.setGeometry(QtCore.QRect(20, 190, 41, 21))
        self.hp.setObjectName("hp")
        self.hp_in1 = QtWidgets.QLineEdit(self.search_tab)
        self.hp_in1.setGeometry(QtCore.QRect(70, 190, 81, 21))
        self.hp_in1.setObjectName("hp_in1")
        self.hp_in2 = QtWidgets.QLineEdit(self.search_tab)
        self.hp_in2.setGeometry(QtCore.QRect(180, 190, 81, 21))
        self.hp_in2.setObjectName("hp_in2")
        self._1 = QtWidgets.QLabel(self.search_tab)
        self._1.setGeometry(QtCore.QRect(160, 190, 16, 21))
        self._1.setObjectName("_1")
        self._2 = QtWidgets.QLabel(self.search_tab)
        self._2.setGeometry(QtCore.QRect(160, 220, 16, 21))
        self._2.setObjectName("_2")
        self.ak = QtWidgets.QCheckBox(self.search_tab)
        self.ak.setGeometry(QtCore.QRect(20, 220, 41, 21))
        self.ak.setObjectName("ak")
        self.ak_in1 = QtWidgets.QLineEdit(self.search_tab)
        self.ak_in1.setGeometry(QtCore.QRect(70, 220, 81, 21))
        self.ak_in1.setObjectName("ak_in1")
        self.ak_in2 = QtWidgets.QLineEdit(self.search_tab)
        self.ak_in2.setGeometry(QtCore.QRect(180, 220, 81, 21))
        self.ak_in2.setObjectName("ak_in2")
        self._3 = QtWidgets.QLabel(self.search_tab)
        self._3.setGeometry(QtCore.QRect(160, 250, 16, 21))
        self._3.setObjectName("_3")
        self.df = QtWidgets.QCheckBox(self.search_tab)
        self.df.setGeometry(QtCore.QRect(20, 250, 41, 21))
        self.df.setObjectName("df")
        self.df_in1 = QtWidgets.QLineEdit(self.search_tab)
        self.df_in1.setGeometry(QtCore.QRect(70, 250, 81, 21))
        self.df_in1.setObjectName("df_in1")
        self.df_in2 = QtWidgets.QLineEdit(self.search_tab)
        self.df_in2.setGeometry(QtCore.QRect(180, 250, 81, 21))
        self.df_in2.setObjectName("df_in2")
        self._4 = QtWidgets.QLabel(self.search_tab)
        self._4.setGeometry(QtCore.QRect(160, 280, 16, 21))
        self._4.setObjectName("_4")
        self.sa = QtWidgets.QCheckBox(self.search_tab)
        self.sa.setGeometry(QtCore.QRect(20, 280, 41, 21))
        self.sa.setObjectName("sa")
        self.sa_in1 = QtWidgets.QLineEdit(self.search_tab)
        self.sa_in1.setGeometry(QtCore.QRect(70, 280, 81, 21))
        self.sa_in1.setObjectName("sa_in1")
        self.sa_in2 = QtWidgets.QLineEdit(self.search_tab)
        self.sa_in2.setGeometry(QtCore.QRect(180, 280, 81, 21))
        self.sa_in2.setObjectName("sa_in2")
        self._5 = QtWidgets.QLabel(self.search_tab)
        self._5.setGeometry(QtCore.QRect(160, 310, 16, 21))
        self._5.setObjectName("_5")
        self.sd = QtWidgets.QCheckBox(self.search_tab)
        self.sd.setGeometry(QtCore.QRect(20, 310, 41, 21))
        self.sd.setObjectName("sd")
        self.sd_in1 = QtWidgets.QLineEdit(self.search_tab)
        self.sd_in1.setGeometry(QtCore.QRect(70, 310, 81, 21))
        self.sd_in1.setObjectName("sd_in1")
        self.sd_in2 = QtWidgets.QLineEdit(self.search_tab)
        self.sd_in2.setGeometry(QtCore.QRect(180, 310, 81, 21))
        self.sd_in2.setObjectName("sd_in2")
        self._6 = QtWidgets.QLabel(self.search_tab)
        self._6.setGeometry(QtCore.QRect(160, 340, 16, 21))
        self._6.setObjectName("_6")
        self.sp = QtWidgets.QCheckBox(self.search_tab)
        self.sp.setGeometry(QtCore.QRect(20, 340, 41, 21))
        self.sp.setObjectName("sp")
        self.sp_in1 = QtWidgets.QLineEdit(self.search_tab)
        self.sp_in1.setGeometry(QtCore.QRect(70, 340, 81, 21))
        self.sp_in1.setObjectName("sp_in1")
        self.sp_in2 = QtWidgets.QLineEdit(self.search_tab)
        self.sp_in2.setGeometry(QtCore.QRect(180, 340, 81, 21))
        self.sp_in2.setObjectName("sp_in2")
        self._7 = QtWidgets.QLabel(self.search_tab)
        self._7.setGeometry(QtCore.QRect(160, 370, 16, 21))
        self._7.setObjectName("_7")
        self.sum = QtWidgets.QCheckBox(self.search_tab)
        self.sum.setGeometry(QtCore.QRect(20, 370, 51, 21))
        self.sum.setObjectName("sum")
        self.sum_in1 = QtWidgets.QLineEdit(self.search_tab)
        self.sum_in1.setGeometry(QtCore.QRect(70, 370, 81, 21))
        self.sum_in1.setObjectName("sum_in1")
        self.sum_in2 = QtWidgets.QLineEdit(self.search_tab)
        self.sum_in2.setGeometry(QtCore.QRect(180, 370, 81, 21))
        self.sum_in2.setObjectName("sum_in2")
        self.stats_label = QtWidgets.QLabel(self.search_tab)
        self.stats_label.setGeometry(QtCore.QRect(20, 155, 241, 21))
        self.stats_label.setObjectName("stats_label")
        # region
        self.rid = QtWidgets.QCheckBox(self.search_tab)
        self.rid.setGeometry(QtCore.QRect(20, 60, 61, 31))
        self.rid.setObjectName("rid")
        self.rid_in1 = QtWidgets.QLineEdit(self.search_tab)
        self.rid_in1.setGeometry(QtCore.QRect(100, 60, 71, 31))
        self.rid_in1.setObjectName("rid_in1")
        self.rid_in2 = QtWidgets.QLineEdit(self.search_tab)
        self.rid_in2.setGeometry(QtCore.QRect(190, 60, 71, 31))
        self.rid_in2.setObjectName("rid_in2")
        self.rname = QtWidgets.QCheckBox(self.search_tab)
        self.rname.setGeometry(QtCore.QRect(20, 110, 71, 31))
        self.rname.setObjectName("rname")
        self.rname_in = QtWidgets.QComboBox(self.search_tab)
        self.rname_in.setGeometry(QtCore.QRect(100, 110, 161, 31))
        self.rname_in.setEditable(True)
        self.rname_in.setObjectName("rname_in")
        # type
        self.tid = QtWidgets.QCheckBox(self.search_tab)
        self.tid.setGeometry(QtCore.QRect(20, 60, 61, 31))
        self.tid.setObjectName("tid")
        self.tid_in1 = QtWidgets.QLineEdit(self.search_tab)
        self.tid_in1.setGeometry(QtCore.QRect(100, 60, 71, 31))
        self.tid_in1.setObjectName("tid_in1")
        self.tid_in2 = QtWidgets.QLineEdit(self.search_tab)
        self.tid_in2.setGeometry(QtCore.QRect(190, 60, 71, 31))
        self.tid_in2.setObjectName("tid_in2")
        self.tname = QtWidgets.QCheckBox(self.search_tab)
        self.tname.setGeometry(QtCore.QRect(20, 110, 71, 31))
        self.tname.setObjectName("tname")
        self.tname_in = QtWidgets.QComboBox(self.search_tab)
        self.tname_in.setGeometry(QtCore.QRect(100, 110, 161, 31))
        self.tname_in.setEditable(True)
        self.tname_in.setObjectName("tname_in")
        # move
        self.mid = QtWidgets.QCheckBox(self.search_tab)
        self.mid.setGeometry(QtCore.QRect(20, 60, 61, 31))
        self.mid.setObjectName("mid")
        self.mid_in1 = QtWidgets.QLineEdit(self.search_tab)
        self.mid_in1.setGeometry(QtCore.QRect(100, 60, 71, 31))
        self.mid_in1.setObjectName("mid_in1")
        self.mid_in2 = QtWidgets.QLineEdit(self.search_tab)
        self.mid_in2.setGeometry(QtCore.QRect(190, 60, 71, 31))
        self.mid_in2.setObjectName("mid_in2")
        self.mname = QtWidgets.QCheckBox(self.search_tab)
        self.mname.setGeometry(QtCore.QRect(20, 110, 71, 31))
        self.mname.setObjectName("mname")
        self.mname_in = QtWidgets.QComboBox(self.search_tab)
        self.mname_in.setGeometry(QtCore.QRect(100, 110, 161, 31))
        self.mname_in.setEditable(True)
        self.mname_in.setObjectName("mname_in")
        self.type_in = QtWidgets.QComboBox(self.search_tab)
        self.type_in.setGeometry(QtCore.QRect(100, 160, 161, 31))
        self.type_in.setEditable(True)
        self.type_in.setObjectName("type_in")
        self.type = QtWidgets.QCheckBox(self.search_tab)
        self.type.setGeometry(QtCore.QRect(20, 160, 71, 31))
        self.type.setObjectName("type")
        self.dclass_in = QtWidgets.QComboBox(self.search_tab)
        self.dclass_in.setGeometry(QtCore.QRect(100, 210, 161, 31))
        self.dclass_in.setEditable(True)
        self.dclass_in.setObjectName("dclass_in")
        self.dclass = QtWidgets.QCheckBox(self.search_tab)
        self.dclass.setGeometry(QtCore.QRect(20, 210, 71, 31))
        self.dclass.setObjectName("dclass")
        self.power = QtWidgets.QCheckBox(self.search_tab)
        self.power.setGeometry(QtCore.QRect(20, 260, 71, 31))
        self.power.setObjectName("power")
        self.power_in = QtWidgets.QComboBox(self.search_tab)
        self.power_in.setGeometry(QtCore.QRect(100, 260, 161, 31))
        self.power_in.setEditable(True)
        self.power_in.setObjectName("power_in")
        self.acc = QtWidgets.QCheckBox(self.search_tab)
        self.acc.setGeometry(QtCore.QRect(20, 310, 71, 31))
        self.acc.setObjectName("acc")
        self.acc_in = QtWidgets.QComboBox(self.search_tab)
        self.acc_in.setGeometry(QtCore.QRect(100, 310, 161, 31))
        self.acc_in.setEditable(True)
        self.acc_in.setObjectName("acc_in")
        self.pp = QtWidgets.QCheckBox(self.search_tab)
        self.pp.setGeometry(QtCore.QRect(20, 360, 71, 31))
        self.pp.setObjectName("pp")
        self.pp_in1 = QtWidgets.QLineEdit(self.search_tab)
        self.pp_in1.setGeometry(QtCore.QRect(100, 360, 71, 31))
        self.pp_in1.setObjectName("pp_in1")
        self.pp_in2 = QtWidgets.QLineEdit(self.search_tab)
        self.pp_in2.setGeometry(QtCore.QRect(190, 360, 71, 31))
        self.pp_in2.setObjectName("pp_in2")
        self._10 = QtWidgets.QLabel(self.search_tab)
        self._10.setGeometry(QtCore.QRect(180, 360, 16, 31))
        self._10.setObjectName("_10")
        # pokemon_moves
        self.pmname = QtWidgets.QCheckBox(self.search_tab)
        self.pmname.setGeometry(QtCore.QRect(20, 60, 71, 31))
        self.pmname.setObjectName("pmname")
        self.pmname_in = QtWidgets.QComboBox(self.search_tab)
        self.pmname_in.setGeometry(QtCore.QRect(100, 60, 161, 31))
        self.pmname_in.setEditable(True)
        self.pmname_in.setObjectName("pmname_in")
        # damage_class
        self.cid = QtWidgets.QCheckBox(self.search_tab)
        self.cid.setGeometry(QtCore.QRect(20, 60, 61, 31))
        self.cid.setObjectName("cid")
        self.cid_in = QtWidgets.QComboBox(self.search_tab)
        self.cid_in.setGeometry(QtCore.QRect(100, 60, 161, 31))
        self.cid_in.setEditable(True)
        self.cid_in.setObjectName("cid_in")
        self.cname = QtWidgets.QCheckBox(self.search_tab)
        self.cname.setGeometry(QtCore.QRect(20, 110, 71, 31))
        self.cname.setObjectName("cname")
        self.cname_in = QtWidgets.QComboBox(self.search_tab)
        self.cname_in.setGeometry(QtCore.QRect(100, 110, 161, 31))
        self.cname_in.setEditable(True)
        self.cname_in.setObjectName("cname_in")
        self.search_btn = QtWidgets.QPushButton(self.search_tab)
        self.search_btn.setGeometry(QtCore.QRect(20, 410, 111, 41))
        self.search_btn.setObjectName("search_btn")
        self.createView_btn = QtWidgets.QPushButton(self.search_tab)
        self.createView_btn.setGeometry(QtCore.QRect(150, 410, 111, 41))
        self.createView_btn.setObjectName("createView_btn")
        self.search_btn.clicked.connect(self.search)
        self.createView_btn.clicked.connect(self.create_view)

        self.pid.setText("Pid")
        self.pname.setText("Pname")
        self.region.setText("region")
        self.type1.setText("type1")
        self.type2.setText("type2")
        self.evolves_from.setText("evolves from")
        self.evolves_into.setText("evolves into")
        self.stats_label.setText("请输入种族值范围：")
        self.hp.setText("HP")
        self.ak.setText("AK")
        self.df.setText("DF")
        self.sa.setText("SA")
        self.sd.setText("SD")
        self.sp.setText("SP")
        self.sum.setText("SUM")
        self.rid.setText("Rid")
        self.rname.setText("Rname")
        self.tid.setText("Tid")
        self.tname.setText("Tname")
        self.mid.setText("Mid")
        self.mname.setText("Mname")
        self.type.setText("type")
        self.dclass.setText("class")
        self.power.setText("power")
        self.acc.setText("acc")
        self.pp.setText("pp")
        self.pmname.setText("Pname")
        self.cid.setText("Cid")
        self.cname.setText("Cname")
        self._1.setText("-")
        self._2.setText("-")
        self._3.setText("-")
        self._4.setText("-")
        self._5.setText("-")
        self._6.setText("-")
        self._7.setText("-")
        self._8.setText("-")  # 最上面
        self._10.setText("-")  # pp
        self.search_btn.setText("查 询")
        self.createView_btn.setText("创建视图")

        self.pokedex_ui = [self.pid,
                           self.pid_in1,
                           self.pid_in2,
                           self._8,
                           self.pname,
                           self.pname_in]
        self.pokemon_ui = [self.pid,
                           self.pid_in1,
                           self.pid_in2,
                           self._8,
                           self.pname,
                           self.pname_in,
                           self.region,
                           self.region_in,
                           self.type1,
                           self.type2,
                           self.type1_in,
                           self.type2_in,
                           self.evolves_from,
                           self.evolves_from_in,
                           self.evolves_into,
                           self.evolves_into_in]
        self.pokemon_stats_ui = [self.pid,
                                 self.pid_in1,
                                 self.pid_in2,
                                 self._8,
                                 self.pname,
                                 self.pname_in,
                                 self.stats_label,
                                 self.hp,
                                 self.ak,
                                 self.df,
                                 self.sa,
                                 self.sd,
                                 self.sp,
                                 self.sum,
                                 self.hp_in1,
                                 self.ak_in1,
                                 self.df_in1,
                                 self.sa_in1,
                                 self.sd_in1,
                                 self.sp_in1,
                                 self.sum_in1,
                                 self.hp_in2,
                                 self.ak_in2,
                                 self.df_in2,
                                 self.sa_in2,
                                 self.sd_in2,
                                 self.sp_in2,
                                 self.sum_in2,
                                 self._1,
                                 self._2,
                                 self._3,
                                 self._4,
                                 self._5,
                                 self._6,
                                 self._7]
        self.region_ui = [self.rid,
                          self.rname,
                          self.rid_in1,
                          self.rid_in2,
                          self._8,
                          self.rname_in]
        self.type_ui = [self.tid,
                        self.tname,
                        self.tid_in1,
                        self.tid_in2,
                        self.tname_in]
        self.move_ui = [self.mid,
                        self.mid_in1,
                        self.mid_in2,
                        self._8,
                        self.mname,
                        self.mname_in,
                        self.type,
                        self.type_in,
                        self.dclass,
                        self.dclass_in,
                        self.power,
                        self.power_in,
                        self.acc,
                        self.acc_in,
                        self.pp,
                        self.pp_in1,
                        self.pp_in2,
                        self._10]
        self.pokemon_moves_ui = [self.pmname,
                                 self.pmname_in,
                                 self.mname,
                                 self.mname_in]
        self.damage_class_ui = [self.cid,
                                self.cid_in,
                                self.cname,
                                self.cname_in]
        self.check_ui = [[[self.pid, self.pid_in1, self.pid_in2],
                          [self.rid, self.rid_in1, self.rid_in2],
                          [self.tid, self.tid_in1, self.tid_in2],
                          [self.mid, self.mid_in1, self.mid_in2],
                          [self.hp, self.hp_in1, self.hp_in2],
                          [self.ak, self.ak_in1, self.ak_in2],
                          [self.df, self.df_in1, self.df_in2],
                          [self.sa, self.sa_in1, self.sa_in2],
                          [self.sd, self.sd_in1, self.sd_in2],
                          [self.sp, self.sp_in1, self.sp_in2],
                          [self.sum, self.sum_in1, self.sum_in2],
                          [self.pp, self.pp_in1, self.pp_in2]],  # lineedit
                         [[self.pname, self.pname_in],
                          [self.region, self.region_in],
                          [self.type1, self.type1_in],
                          [self.type2, self.type2_in],
                          [self.evolves_from, self.evolves_from_in],
                          [self.evolves_into, self.evolves_into_in],
                          [self.rname, self.rname_in],
                          [self.tname, self.tname_in],
                          [self.mname, self.mname_in],
                          [self.type, self.type_in],
                          [self.dclass, self.dclass_in],
                          [self.power, self.power_in],
                          [self.acc, self.acc_in],
                          [self.pmname, self.pmname_in],
                          [self.cid, self.cid_in],
                          [self.cname, self.cname_in]]]  # combotext
        self.label_ui = [self.stats_label,
                         self._1,
                         self._2,
                         self._3,
                         self._4,
                         self._5,
                         self._6,
                         self._7,
                         self._8,  # 最上面
                         self._10]  # pp

        # self._hide_all_search_ui()
        self._pokedex_ui()

    def _special_search_ui(self):
        self.special_search_tab = QtWidgets.QWidget()
        self.special_search_tab.setObjectName("special_search_tab")
        self.specialSelectBox = QtWidgets.QComboBox(self.special_search_tab)
        self.specialSelectBox.setGeometry(QtCore.QRect(20, 10, 241, 31))
        self.specialSelectBox.setEditable(False)
        self.specialSelectBox.setObjectName("specialSelectBox")
        self.specialSelectBox.addItem("连接查询")
        self.specialSelectBox.addItem("嵌套查询")
        self.specialSelectBox.addItem("分组查询")
        self.specialSelectBox.currentIndexChanged.connect(self._selection_change)
        self.specialCreateView_btn = QtWidgets.QPushButton(self.special_search_tab)
        self.specialCreateView_btn.setGeometry(QtCore.QRect(150, 410, 111, 41))
        self.specialCreateView_btn.setObjectName("specialCreateView_btn")
        self.specialSearch_btn = QtWidgets.QPushButton(self.special_search_tab)
        self.specialSearch_btn.setGeometry(QtCore.QRect(20, 410, 111, 41))
        self.specialSearch_btn.setObjectName("specialSearch_btn")
        self.specialCreateView_btn.setText("创建视图")
        self.specialSearch_btn.setText("查 询")
        self.specialSearch_btn.clicked.connect(self.special_search)
        self.specialCreateView_btn.clicked.connect(self.create_view)
        self.searchTabWidget.addTab(self.special_search_tab, "特殊查询")

        # 连接查询
        self.selectBox_join1 = QtWidgets.QComboBox(self.special_search_tab)
        self.selectBox_join1.setGeometry(QtCore.QRect(100, 60, 161, 31))
        self.selectBox_join1.setEditable(False)
        self.selectBox_join1.setObjectName("selectBox_join1")
        self.selectBox_join1.addItem("——")
        self.selectBox_join1.addItem("pokedex")
        self.selectBox_join1.addItem("pokemon")
        self.selectBox_join1.addItem("pokemon_stats")
        self.selectBox_join1.addItem("region")
        self.selectBox_join1.addItem("type")
        self.selectBox_join1.addItem("move")
        self.selectBox_join1.addItem("pokemon_moves")
        self.selectBox_join1.addItem("damage_class")
        self.selectLabel_join1 = QtWidgets.QLabel(self.special_search_tab)
        self.selectLabel_join1.setGeometry(QtCore.QRect(20, 60, 71, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(9)
        self.selectLabel_join1.setFont(font)
        self.selectLabel_join1.setObjectName("selectLabel_join1")
        self.selectBox_join2 = QtWidgets.QComboBox(self.special_search_tab)
        self.selectBox_join2.setGeometry(QtCore.QRect(100, 110, 161, 31))
        self.selectBox_join2.setEditable(False)
        self.selectBox_join2.setObjectName("selectBox_join2")
        self.selectLabel_join2 = QtWidgets.QLabel(self.special_search_tab)
        self.selectLabel_join2.setGeometry(QtCore.QRect(20, 110, 71, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(9)
        self.selectLabel_join2.setFont(font)
        self.selectLabel_join2.setObjectName("selectLabel_join2")
        self.selectBox_join3 = QtWidgets.QComboBox(self.special_search_tab)
        self.selectBox_join3.setGeometry(QtCore.QRect(20, 190, 241, 31))
        self.selectBox_join3.setEditable(False)
        self.selectBox_join3.setObjectName("selectBox_join3")
        self.selectLabel_join3 = QtWidgets.QLabel(self.special_search_tab)
        self.selectLabel_join3.setGeometry(QtCore.QRect(20, 160, 121, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(9)
        self.selectLabel_join3.setFont(font)
        self.selectLabel_join3.setObjectName("selectLabel_join3")

        self.selectLabel_join1.setText("请选择表1")
        self.selectLabel_join2.setText("请选择表2")
        self.selectLabel_join3.setText("请选择查询条件")

        self.selectBox_join1.currentIndexChanged.connect(self._join1_select_change)

        self.join_search_ui = [self.selectLabel_join1,
                               self.selectLabel_join2,
                               self.selectLabel_join3,
                               self.selectBox_join1,
                               self.selectBox_join2,
                               self.selectBox_join3]

        # 嵌套查询
        self.in_search_ui = []

        # 分组查询
        self.selectBox_group1 = QtWidgets.QComboBox(self.special_search_tab)
        self.selectBox_group1.setGeometry(QtCore.QRect(20, 90, 241, 31))
        self.selectBox_group1.setEditable(False)
        self.selectBox_group1.setObjectName("selectBox_group1")
        self.selectBox_group1.addItem("——")
        self.selectBox_group1.addItem("pokemon_stats")
        self.selectBox_group1.addItem("move")
        self.selectLabel_group1 = QtWidgets.QLabel(self.special_search_tab)
        self.selectLabel_group1.setGeometry(QtCore.QRect(20, 60, 201, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(9)
        self.selectLabel_group1.setFont(font)
        self.selectLabel_group1.setObjectName("selectLabel_group1")
        self.selectBox_group2 = QtWidgets.QComboBox(self.special_search_tab)
        self.selectBox_group2.setGeometry(QtCore.QRect(20, 170, 241, 31))
        self.selectBox_group2.setEditable(False)
        self.selectBox_group2.setObjectName("selectBox_group2")
        self.selectLabel_group2 = QtWidgets.QLabel(self.special_search_tab)
        self.selectLabel_group2.setGeometry(QtCore.QRect(20, 140, 201, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(9)
        self.selectLabel_group2.setFont(font)
        self.selectLabel_group2.setObjectName("selectLabel_group2")

        self.selectLabel_group1.setText("请选择查询的表")
        self.selectLabel_group2.setText("请选择用于分组的属性")

        self.selectBox_group1.currentIndexChanged.connect(self._group1_select_change)

        self.group_search_ui = [self.selectLabel_group1,
                                self.selectLabel_group2,
                                self.selectBox_group1,
                                self.selectBox_group2]

        # self._hide_all_special_search_ui()
        self._join_search_ui()

    def _index_ui(self):
        self.index_tab = QtWidgets.QWidget()
        self.index_tab.setObjectName("index_tab")
        self.createIndex_btn = QtWidgets.QPushButton(self.index_tab)
        self.createIndex_btn.setGeometry(QtCore.QRect(20, 410, 111, 41))
        self.createIndex_btn.setObjectName("createIndex_btn")
        self.indexSelectBox1 = QtWidgets.QComboBox(self.index_tab)
        self.indexSelectBox1.setGeometry(QtCore.QRect(20, 50, 241, 31))
        self.indexSelectBox1.setEditable(False)
        self.indexSelectBox1.setObjectName("indexSelectBox1")
        self.indexSelectBox1.addItem("——")
        self.indexSelectBox1.addItem("pokedex")
        self.indexSelectBox1.addItem("pokemon")
        self.indexSelectBox1.addItem("pokemon_stats")
        self.indexSelectBox1.addItem("region")
        self.indexSelectBox1.addItem("typw")
        self.indexSelectBox1.addItem("move")
        self.indexSelectBox1.addItem("pokemon_moves")
        self.indexSelectBox1.addItem("damage_class")
        self.indexLabel1 = QtWidgets.QLabel(self.index_tab)
        self.indexLabel1.setGeometry(QtCore.QRect(20, 20, 201, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(9)
        self.indexLabel1.setFont(font)
        self.indexLabel1.setObjectName("indexLabel1")
        self.indexSelectBox2 = QtWidgets.QComboBox(self.index_tab)
        self.indexSelectBox2.setGeometry(QtCore.QRect(20, 130, 241, 31))
        self.indexSelectBox2.setEditable(False)
        self.indexSelectBox2.setObjectName("indexSelectBox2")
        self.indexLabel2 = QtWidgets.QLabel(self.index_tab)
        self.indexLabel2.setGeometry(QtCore.QRect(20, 100, 201, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(9)
        self.indexLabel2.setFont(font)
        self.indexLabel2.setObjectName("indexLabel2")
        self.showIndexes_btn = QtWidgets.QPushButton(self.index_tab)
        self.showIndexes_btn.setGeometry(QtCore.QRect(150, 410, 111, 41))
        self.showIndexes_btn.setObjectName("showIndexes_btn")
        self.indexEdit = QtWidgets.QTextEdit(self.index_tab)
        self.indexEdit.setGeometry(QtCore.QRect(20, 190, 241, 131))
        self.indexEdit.setObjectName("indexEdit")
        self.indexNameLabel = QtWidgets.QLabel(self.index_tab)
        self.indexNameLabel.setGeometry(QtCore.QRect(30, 350, 51, 31))
        self.indexNameLabel.setObjectName("indexNameLabel")
        self.indexNameEdit = QtWidgets.QLineEdit(self.index_tab)
        self.indexNameEdit.setGeometry(QtCore.QRect(92, 350, 161, 31))
        self.indexNameEdit.setObjectName("indexNameEdit")
        self.searchTabWidget.addTab(self.index_tab, "索引")

        self.indexLabel1.setText("请选择表")
        self.indexLabel2.setText("请选择属性")
        self.createIndex_btn.setText("创建索引")
        self.showIndexes_btn.setText("索引列表")
        self.indexNameLabel.setText("索引名")

        self.indexSelectBox1.currentIndexChanged.connect(self._index1_select_change)
        self.createIndex_btn.clicked.connect(self.create_index)
        self.showIndexes_btn.clicked.connect(self.show_indexes)

    def _hide_all_search_ui(self):
        for ui_set in self.check_ui[0]:
            for ui in ui_set:
                ui.hide()
        for ui_set in self.check_ui[1]:
            for ui in ui_set:
                ui.hide()
        for ui in self.label_ui:
            ui.hide()
        self.search_btn.hide()
        self.createView_btn.hide()

    def _hide_all_special_search_ui(self):
        for ui in self.join_search_ui:
            ui.hide()
        for ui in self.in_search_ui:
            ui.hide()
        for ui in self.group_search_ui:
            ui.hide()
        self.specialSearch_btn.hide()
        self.specialCreateView_btn.hide()

    def _clear_all_search_in(self):
        for ui_set in self.check_ui[0]:
            for ui in ui_set[1:]:
                ui.clear()
        for ui_set in self.check_ui[1]:
            for ui in ui_set[1:]:
                ui.clearEditText()

    def _uncheck_all_check_ui(self):
        for ui_set in self.check_ui[0]:
            ui_set[0].setChecked(False)
        for ui_set in self.check_ui[1]:
            ui_set[0].setChecked(False)

    def _selection_change(self):
        if self.searchTabWidget.currentWidget() == self.search_tab:
            if self.selectBox.currentText() == "pokedex":
                self._pokedex_ui()
            elif self.selectBox.currentText() == "pokemon":
                self._pokemon_ui()
            elif self.selectBox.currentText() == "pokemon_stats":
                self._pokemon_stats_ui()
            elif self.selectBox.currentText() == "region":
                self._region_ui()
            elif self.selectBox.currentText() == "type":
                self._type_ui()
            elif self.selectBox.currentText() == "move":
                self._move_ui()
            elif self.selectBox.currentText() == "pokemon_moves":
                self._pokemon_moves_ui()
            else:
                self._damage_class_ui()
        elif self.searchTabWidget.currentWidget() == self.special_search_tab:
            if self.specialSelectBox.currentText() == "连接查询":
                self._join_search_ui()
            elif self.specialSelectBox.currentText() == "嵌套查询":
                self._in_search_ui()
            else:
                self._group_search_ui()

    def _join1_select_change(self):
        if self.selectBox_join1.currentText() == "pokedex":
            self.selectBox_join2.clear()
            self.selectBox_join3.clear()
            self.selectBox_join2.addItem("——")
            self.selectBox_join2.addItem("pokemon")
            self.selectBox_join2.addItem("pokemon_stats")
            self.selectBox_join2.addItem("pokemon_move")
        elif self.selectBox_join1.currentText() == "pokemon":
            self.selectBox_join2.clear()
            self.selectBox_join3.clear()
            self.selectBox_join2.addItem("——")
            self.selectBox_join2.addItem("pokedex")
            self.selectBox_join2.addItem("region")
            self.selectBox_join2.addItem("type")
        elif self.selectBox_join1.currentText() == "pokemon_stats":
            self.selectBox_join2.clear()
            self.selectBox_join3.clear()
            self.selectBox_join2.addItem("——")
            self.selectBox_join2.addItem("pokedex")
        elif self.selectBox_join1.currentText() == "region":
            self.selectBox_join2.clear()
            self.selectBox_join3.clear()
            self.selectBox_join2.addItem("——")
            self.selectBox_join2.addItem("pokemon")
        elif self.selectBox_join1.currentText() == "type":
            self.selectBox_join2.clear()
            self.selectBox_join3.clear()
            self.selectBox_join2.addItem("——")
            self.selectBox_join2.addItem("pokemon")
            self.selectBox_join2.addItem("move")
        elif self.selectBox_join1.currentText() == "move":
            self.selectBox_join2.clear()
            self.selectBox_join3.clear()
            self.selectBox_join2.addItem("——")
            self.selectBox_join2.addItem("type")
            self.selectBox_join2.addItem("pokemon_moves")
            self.selectBox_join2.addItem("damage_class")
        elif self.selectBox_join1.currentText() == "pokemon_moves":
            self.selectBox_join2.clear()
            self.selectBox_join3.clear()
            self.selectBox_join2.addItem("——")
            self.selectBox_join2.addItem("pokedex")
            self.selectBox_join2.addItem("move")
        elif self.selectBox_join1.currentText() == "damage_class":
            self.selectBox_join2.clear()
            self.selectBox_join3.clear()
            self.selectBox_join2.addItem("——")
            self.selectBox_join2.addItem("move")

        self.selectBox_join2.currentIndexChanged.connect(self._join2_select_change)

    def _join2_select_change(self):
        if self.selectBox_join1.currentText() == "pokedex":
            if self.selectBox_join2.currentText() == "pokemon":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("Pname<->Pname")
                self.selectBox_join3.addItem("Pname<->evolves_from")
                self.selectBox_join3.addItem("Pname<->evolves_into")
            elif self.selectBox_join2.currentText() == "pokemon_stats":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("Pname<->Pname")
            elif self.selectBox_join2.currentText() == "pokemon_moves":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("Pname<->Pname")
        elif self.selectBox_join1.currentText() == "pokemon":
            if self.selectBox_join2.currentText() == "pokedex":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("Pname<->Pname")
                self.selectBox_join3.addItem("evolves_from<->Pname")
                self.selectBox_join3.addItem("evolves_into<->Pname")
            elif self.selectBox_join2.currentText() == "region":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("region<->Rname")
            elif self.selectBox_join2.currentText() == "type":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("type1<->Tname")
                self.selectBox_join3.addItem("type2<->Tname")
        elif self.selectBox_join1.currentText() == "pokemon_stats":
            if self.selectBox_join2.currentText() == "pokedex":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("Pname<->Pname")
        elif self.selectBox_join1.currentText() == "region":
            if self.selectBox_join2.currentText() == "pokemon":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("Rname<->region")
        elif self.selectBox_join1.currentText() == "type":
            if self.selectBox_join2.currentText() == "pokemon":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("Tname<->type1")
                self.selectBox_join3.addItem("Tname<->type2")
            elif self.selectBox_join2.currentText() == "move":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("Tname<->type")
        elif self.selectBox_join1.currentText() == "move":
            if self.selectBox_join2.currentText() == "type":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("type<->Tname")
            elif self.selectBox_join2.currentText() == "pokemon_moves":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("Mname<->Mname")
            elif self.selectBox_join2.currentText() == "damage_class":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("class<->Cname")
        elif self.selectBox_join1.currentText() == "pokemon_moves":
            if self.selectBox_join2.currentText() == "pokedex":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("Pname<->Pname")
            elif self.selectBox_join2.currentText() == "move":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("Mname<->Mname")
        elif self.selectBox_join1.currentText() == "damage_class":
            if self.selectBox_join2.currentText() == "move":
                self.selectBox_join3.clear()
                self.selectBox_join3.addItem("Cname<->class")

    def _group1_select_change(self):
        if self.selectBox_group1.currentText() == "pokemon_stats":
            self.selectBox_group2.clear()
            self.selectBox_group2.addItem("HP")
            self.selectBox_group2.addItem("AK")
            self.selectBox_group2.addItem("DF")
            self.selectBox_group2.addItem("SA")
            self.selectBox_group2.addItem("SD")
            self.selectBox_group2.addItem("SP")
            self.selectBox_group2.addItem("SUM")
        elif self.selectBox_group1.currentText() == "move":
            self.selectBox_group2.clear()
            self.selectBox_group2.addItem("type")
            self.selectBox_group2.addItem("class")
            self.selectBox_group2.addItem("power")
            self.selectBox_group2.addItem("acc")
            self.selectBox_group2.addItem("pp")

    def _index1_select_change(self):
        if self.indexSelectBox1.currentText() == "——":
            return
        if self.indexSelectBox1.currentText() == "pokedex":
            self.indexSelectBox2.clear()
            self.indexSelectBox2.addItem("——")
            self.indexSelectBox2.addItem("Pid")
            self.indexSelectBox2.addItem("Pname")
        elif self.indexSelectBox1.currentText() == "pokemon":
            self.indexSelectBox2.clear()
            self.indexSelectBox2.addItem("——")
            self.indexSelectBox2.addItem("Pid")
            self.indexSelectBox2.addItem("Pname")
            self.indexSelectBox2.addItem("region")
            self.indexSelectBox2.addItem("type1")
            self.indexSelectBox2.addItem("type2")
            self.indexSelectBox2.addItem("evolves from")
            self.indexSelectBox2.addItem("evolves into")
        elif self.indexSelectBox1.currentText() == "pokemon_stats":
            self.indexSelectBox2.clear()
            self.indexSelectBox2.addItem("——")
            self.indexSelectBox2.addItem("Pid")
            self.indexSelectBox2.addItem("Pname")
            self.indexSelectBox2.addItem("HP")
            self.indexSelectBox2.addItem("AK")
            self.indexSelectBox2.addItem("DF")
            self.indexSelectBox2.addItem("SA")
            self.indexSelectBox2.addItem("SD")
            self.indexSelectBox2.addItem("SP")
            self.indexSelectBox2.addItem("SUM")
        elif self.indexSelectBox1.currentText() == "region":
            self.indexSelectBox2.clear()
            self.indexSelectBox2.addItem("——")
            self.indexSelectBox2.addItem("Rid")
            self.indexSelectBox2.addItem("Rname")
        elif self.indexSelectBox1.currentText() == "type":
            self.indexSelectBox2.clear()
            self.indexSelectBox2.addItem("——")
            self.indexSelectBox2.addItem("Tid")
            self.indexSelectBox2.addItem("Tname")
        elif self.indexSelectBox1.currentText() == "move":
            self.indexSelectBox2.clear()
            self.indexSelectBox2.addItem("——")
            self.indexSelectBox2.addItem("Mid")
            self.indexSelectBox2.addItem("Mname")
            self.indexSelectBox2.addItem("type")
            self.indexSelectBox2.addItem("class")
            self.indexSelectBox2.addItem("power")
            self.indexSelectBox2.addItem("acc")
            self.indexSelectBox2.addItem("pp")
        elif self.indexSelectBox1.currentText() == "pokemon_moves":
            self.indexSelectBox2.clear()
            self.indexSelectBox2.addItem("——")
            self.indexSelectBox2.addItem("Pname")
            self.indexSelectBox2.addItem("Mname")
        elif self.indexSelectBox1.currentText() == "damage_class":
            self.indexSelectBox2.clear()
            self.indexSelectBox2.addItem("——")
            self.indexSelectBox2.addItem("Cid")
            self.indexSelectBox2.addItem("Cname")
        self.indexEdit.clear()
        self.indexSelectBox2.currentIndexChanged.connect(self._index2_select_change)

    def _index2_select_change(self):
        if self.indexSelectBox2.currentText() != "——":
            print(self.indexSelectBox2.currentText())
            field = self.indexSelectBox2.currentText()
            self.indexEdit.insertPlainText(field + "\n")

    def _pokedex_ui(self):
        self._uncheck_all_check_ui()
        self._clear_all_search_in()
        self._hide_all_search_ui()
        for ui in self.pokedex_ui:
            ui.show()
        self.search_btn.show()
        self.createView_btn.show()

    def _pokemon_ui(self):
        self._uncheck_all_check_ui()
        self._clear_all_search_in()
        self._hide_all_search_ui()
        for ui in self.pokemon_ui:
            ui.show()
        self.search_btn.show()
        self.createView_btn.show()

    def _pokemon_stats_ui(self):
        self._uncheck_all_check_ui()
        self._clear_all_search_in()
        self._hide_all_search_ui()
        for ui in self.pokemon_stats_ui:
            ui.show()
        self.search_btn.show()
        self.createView_btn.show()

    def _region_ui(self):
        self._uncheck_all_check_ui()
        self._clear_all_search_in()
        self._hide_all_search_ui()
        for ui in self.region_ui:
            ui.show()
        self.search_btn.show()
        self.createView_btn.show()

    def _type_ui(self):
        self._uncheck_all_check_ui()
        self._clear_all_search_in()
        self._hide_all_search_ui()
        for ui in self.type_ui:
            ui.show()
        self.search_btn.show()
        self.createView_btn.show()

    def _move_ui(self):
        self._uncheck_all_check_ui()
        self._clear_all_search_in()
        self._hide_all_search_ui()
        for ui in self.move_ui:
            ui.show()
        self.search_btn.show()
        self.createView_btn.show()

    def _pokemon_moves_ui(self):
        self._uncheck_all_check_ui()
        self._clear_all_search_in()
        self._hide_all_search_ui()
        for ui in self.pokemon_moves_ui:
            ui.show()
        self.search_btn.show()
        self.createView_btn.show()

    def _damage_class_ui(self):
        self._uncheck_all_check_ui()
        self._clear_all_search_in()
        self._hide_all_search_ui()
        for ui in self.damage_class_ui:
            ui.show()
        self.search_btn.show()

    def _join_search_ui(self):
        self._hide_all_special_search_ui()
        for ui in self.join_search_ui:
            ui.show()
        self.specialSearch_btn.show()
        self.specialCreateView_btn.show()

    def _in_search_ui(self):
        self._hide_all_special_search_ui()
        for ui in self.in_search_ui:
            ui.show()
        self.specialSearch_btn.show()
        self.specialCreateView_btn.show()

    def _group_search_ui(self):
        self._hide_all_special_search_ui()
        for ui in self.group_search_ui:
            ui.show()
        self.specialSearch_btn.show()
        self.specialCreateView_btn.show()

    # def add_child_search(self):
    #     global windows, windows_idx
    #     child_window = ChildWindow()
    #     windows.append(child_window)
    #     windows_idx[child_window] = len(windows)-1
    #     child_window.show()

    def search(self):
        try:
            self.error_label.clear()
            table = self.selectBox.currentText()
            name = []
            values = []
            col_names = self.sql("desc " + table)
            for item in col_names:
                name.append(item[0])
            for ui_set in self.check_ui[0]:
                # if ui_set[0].isChecked():
                #     name.append(ui_set[0].text())
                if ui_set[1].text() != "":
                    values.append(ui_set[0].text() + " >= " + ui_set[1].text())
                if ui_set[2].text() != "":
                    values.append(ui_set[0].text() + " <= " + ui_set[2].text())
            for ui_set in self.check_ui[1]:
                # if ui_set[0].isChecked():
                #     name.append(ui_set[0].text())
                if ui_set[1].currentText() != "":
                    values.append(ui_set[0].text() + " = \"" + ui_set[1].currentText() + "\"")
            cmd = "SELECT " + ", ".join(name) + "\n" + \
                  "FROM " + table + "\n" + \
                  "WHERE " + " and ".join(values) + "\n" + \
                  "ORDER BY " + name[0]
            print(cmd)
            result = self.sql(cmd)
        except Exception as e:
            self.error_label.setText(str(e))
            return

        self.output_search_result(self.cursor.description, result)

    def special_search(self):
        try:
            cmd = ""
            if self.specialSelectBox.currentText() == "连接查询":
                table1 = self.selectBox_join1.currentText()
                table2 = self.selectBox_join2.currentText()
                value1 = table1 + "." + self.selectBox_join3.currentText().split("<->")[0]
                value2 = table2 + "." + self.selectBox_join3.currentText().split("<->")[1]
                name = []
                col_names = self.sql("desc " + table1)
                for item in col_names:
                    if item[0] not in name:
                        name.append(table1 + "." + item[0])
                col_names = self.sql("desc " + table2)
                for item in col_names:
                    if item[0] not in name:
                        name.append(table2 + "." + item[0])
                # 内连接
                cmd = "SELECT " + ", ".join(name) + "\n" + \
                      "FROM " + table1 + " INNER JOIN " + table2 + "\n" + \
                      "ON " + value1 + " = " + value2 + "\n" + \
                      "ORDER BY " + name[0]
            elif self.specialSelectBox.currentText() == "嵌套查询":
                pass
            else:  # 分组查询
                table = self.selectBox_group1.currentText()
                group_by = self.selectBox_group2.currentText()
                name = []
                col_names = self.sql("desc " + table)
                for item in col_names:
                    if item[0] in ["Pname", "Mname"]:
                        name.append("GROUP_CONCAT(" + item[0] + ")")
                    else:
                        name.append(item[0])
                cmd = "SELECT " + ", ".join(name) + "\n" + \
                      "FROM " + table + "\n" + \
                      "GROUP BY " + group_by + "\n" + \
                      "ORDER BY " + name[0]
            print(cmd)
            result = self.sql(cmd)
        except Exception as e:
            self.error_label.setText(str(e))
            return

        self.output_search_result(self.cursor.description, result)

    def output_search_result(self, names, data):
        if "search_result" not in self.opened_tables.keys():
            tab = QtWidgets.QWidget()
            tab.setObjectName("search_result")
            scrollArea = QtWidgets.QScrollArea(tab)
            scrollArea.setGeometry(QtCore.QRect(0, 30, 791, 741))
            scrollArea.setWidgetResizable(True)
            scrollArea.setObjectName("scrollArea")
            scrollAreaWidgetContents = QtWidgets.QWidget()
            scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 789, 739))
            scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
            # 创建表格
            table_info = QtWidgets.QTableWidget(scrollAreaWidgetContents)
            table_info.setGeometry(QtCore.QRect(0, 0, 791, 741))
            table_info.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            table_info.setObjectName("table_info")
            scrollArea.setWidget(scrollAreaWidgetContents)
            self.tabWidget.addTab(tab, "")
            self.tabWidget.setTabText(self.tabWidget.indexOf(tab), "搜索结果")

            self.opened_tables["search_result"] = table_info

        else:
            table_info = self.opened_tables["search_result"]

        table_info.clear()
        row_num = len(data)
        col_num = len(names)
        table_info.setColumnCount(col_num)
        table_info.setRowCount(row_num)
        col = 0
        for name in names:
            tw_item = QtWidgets.QTableWidgetItem(name[0])
            table_info.setHorizontalHeaderItem(col, tw_item)
            col += 1

        data_size = len(data)
        if not data_size == 0:
            # print(data)
            table_info.setRowCount(data_size)
            for i in range(data_size):
                for j in range(len(names)):
                    item = QtWidgets.QTableWidgetItem(str(data[i][j]))
                    item.setTextAlignment(Qt.AlignCenter)
                    table_info.setItem(i, j, item)  # row,column都是从0开始
        table_info.show()

    def create_view(self):
        global windows
        name_win = NameWindow()
        windows.append(name_win)
        name_win.show()

    def create_index(self):
        try:
            fields = self.indexEdit.toPlainText().strip().split("\n")
            table = self.indexSelectBox1.currentText()
            index_name = self.indexNameEdit.text()
            if index_name == "":
                self.error_label.setText("未输入索引名！")
                return
            cmd = "CREATE INDEX %s ON %s(%s)" % (index_name, table, ", ".join(fields))
            print(cmd)
            self.sql(cmd)
        except Exception as e:
            self.error_label.setText(str(e))
            return

    def show_indexes(self):
        try:
            self.indexEdit.clear()
            table = self.indexSelectBox1.currentText()
            if table == "——":
                return
            cmd = "show index from " + table
            result = self.sql(cmd)
            for item in result:
                self.indexEdit.insertPlainText(item[2] + " -> " + str(item[4]) + "\n")
        except Exception as e:
            self.error_label.setText(str(e))
            return

    def show_sql(self, cmd):
        self.sql_text.setText(cmd)

    def sql(self, cmd):
        self.show_sql(cmd)
        if self.is_connect:
            self.cursor.execute(cmd)
            self.db.commit()
            return self.cursor.fetchall()
        else:
            print("==== unconnect ====")


class NameWindow(QDialog, Ui_NameDialog):
    def __init__(self, parent=None):
        super(NameWindow, self).__init__(parent)
        self.setupUi(self)
        self.name = ""
        self.accept_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.cancel)

    def accept(self):
        self.name = self.nameEdit.text()
        global main_window
        view_name = self.name
        cmd = "CREATE VIEW " + view_name + " AS\n" + main_window.sql_text.toPlainText()
        try:
            main_window.sql(cmd)
        except Exception as e:
            main_window.error_label.setText(str(e))
            return
        self.close()

    def cancel(self):
        self.close()


class ChildWindow(QDialog, Ui_ChildDialog):
    def __init__(self, parent=None):
        super(ChildWindow, self).__init__(parent)
        self.setupUi(self)
        global main_window
        self.add_child_search_btn.clicked.connect(main_window.add_child_search)
        self.accept_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.cancel)

    def accept(self):
        global windows, windows_idx
        parent_window = windows[windows_idx[self]-1]
        cmd = ""
        if not self.select_in.toPlainText() == "":
            cmd += self.select_label.text() + " " + self.select_in.toPlainText() + "\n"
        if not self.from_in.toPlainText() == "":
            cmd += self.from_label.text() + " " + self.from_in.toPlainText() + "\n"
        if not self.where_in.toPlainText() == "":
            cmd += self.where_label.text() + " " + self.where_in.toPlainText() + "\n"
        if not self.groupby_in.toPlainText() == "":
            cmd += self.groupby_label.text() + " " + self.groupby_in.toPlainText() + "\n"
        if not self.having_in.toPlainText() == "":
            cmd += self.having_label.text() + " " + self.having_in.toPlainText() + "\n"
        if not self.orderby_in.toPlainText() == "":
            cmd += self.orderby_label.text() + " " + self.orderby_in.toPlainText() + "\n"
        cmd = " (" + cmd + ") "
        parent_window.where_in.insertPlainText(cmd)
        windows.pop()
        self.close()

    def cancel(self):
        global windows, windows_idx
        windows.pop()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PokebaseApp()
    windows = [main_window]
    windows_idx = {}
    windows_idx[main_window] = 0
    parent_window = None
    main_window.show()
    sys.exit(app.exec_())
