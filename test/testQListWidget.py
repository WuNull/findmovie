import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    """
    自动生成的代码, 请不要修改
    """
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(455, 357)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 341, 341))
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(360, 10, 81, 31))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))


class Windows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Windows, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.deal)

    def deal(self):
        all_data = json.loads('[{"ship_name":"\u6d4b\u8bd5","ship_index":"1","ship_photo":"icon/2.png"}]')
        def get_item_wight(data):
            # 读取属性
            ship_name = data['ship_name']
            ship_photo = data['ship_photo']
            ship_index = data['ship_index']
            # 总Widget
            wight = QWidget()

            # 总体横向布局
            layout_main = QHBoxLayout()
            # 三列
            layout_main.addWidget(QLabel(ship_name))
            layout_main.addWidget(QLabel(ship_photo))
            layout_main.addWidget(QLabel(str(ship_index) + "星"))

            wight.setLayout(layout_main)  # 布局给wight
            return wight  # 返回wight

        for ship_data in all_data:
            item = QListWidgetItem()  # 创建QListWidgetItem对象
            item.setSizeHint(QSize(200, 50))  # 设置QListWidgetItem大小
            widget = get_item_wight(ship_data)  # 调用上面的函数获取对应
            self.listWidget.addItem(item)  # 添加item
            self.listWidget.setItemWidget(item, widget)  # 为item设置widget


app = QtWidgets.QApplication(sys.argv)
windows = Windows()
windows.show()
sys.exit(app.exec_())
