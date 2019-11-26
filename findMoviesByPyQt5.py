"""
python-version: 3.8.0
查找电影 小工具
实现思路:
1.实现电影资源网站的搜索功能
2.获取搜索结果的网页信息
3.进入电影详情页面获取播放和下载地址
"""
# coding=utf-8
import sys
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QPushButton, QLineEdit, QListWidget, QGridLayout, QMessageBox, QApplication, \
    QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QPixmap, QImage
from utils.findMovieSource import search_movie

# 图片窗口
class ImageWindow(QMainWindow):
    def __init__(self, resources, title):
        super(ImageWindow, self).__init__()
        self.setWindowTitle(title)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        image = QImage(resources)
        pixmap = QPixmap(resources)
        image_label = QLabel(self)
        image_label.setPixmap(pixmap)
        image_label.resize(pixmap.width(), pixmap.height())
        layout.addWidget(image_label)

# pyqt5 主窗口数据
class LayoutDialog(QMainWindow):
    __slots__ = ['word', 'movie_name_label', 'movie_name_line_edit', 'movie_source_label', 'movie_source_combobox',
                 'search_push_button', 'tip_label', 'search_content_label', 'search_content_text_list']

    def __init__(self):
        super().__init__()
        self.left = 400
        self.top = 400
        self.width = 800
        self.height = 600

        self.work = WorkThread()
        # 初始化窗口数据
        self.init_widgets().init_layout().init_event()

    # pyqt5 窗口居中
    def center(self):
        screen = QDesktopWidget().screenGeometry()  # 获取屏幕分辨率
        size = self.geometry()  # 获取窗口尺寸
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)  # 利用move函数窗口居中

    def init_widgets(self):
        # 设置窗口标题
        self.setWindowTitle(self.tr("搜索电影 v1.0"))
        self.setGeometry(self.left, self.top, self.width, self.height)
        # 窗口居中显示
        self.center()

        self.movie_name_label = QLabel(self.tr("电影名称:"))
        # 编辑框
        qle = QLineEdit()
        # 编辑提示语
        qle.setPlaceholderText("请输入需要搜索的关键字")
        self.movie_name_line_edit = qle

        # 多资源下拉框
        # self.movie_source_label = QLabel(self.tr("选择片源:"))
        # self.movie_source_combobox = QComboBox()
        # self.movie_source_combobox.addItem(self.tr('电影天堂'))

        # 查询按钮
        self.search_push_button = QPushButton(self.tr("搜索"))

        # 查询提示
        self.tip_label = QLabel(self.tr("等待搜索..."))
        self.search_content_label = QLabel(self.tr("搜索状态:"))
        # 查询结果展示
        self.search_content_text_list = QListWidget()

        self.menu_bar = self.menuBar()

        return self

    # 窗口布局
    def init_layout(self):
        # QGridLayout：格栅布局，也被称作网格布局（多行多列）。
        top_layout = QGridLayout()
        # 电影名称
        top_layout.addWidget(self.movie_name_label, 0, 0)
        # 搜索内容狂
        top_layout.addWidget(self.movie_name_line_edit, 0, 1)

        # 备选资源框
        # top_layout.addWidget(self.movie_source_label, 0, 2)
        # top_layout.addWidget(self.movie_source_combobox, 0, 3)

        # 查询按钮
        top_layout.addWidget(self.search_push_button, 0, 4)
        # 提示框
        top_layout.addWidget(self.tip_label, 3, 1)
        # 搜索状态提示
        top_layout.addWidget(self.search_content_label, 3, 0)
        # 查询内容展示
        top_layout.addWidget(self.search_content_text_list, 4, 0, 2, 5)

        # 查询结果展示窗口
        main_frame = QWidget()
        # 横向三列布局
        self.setCentralWidget(main_frame)
        main_frame.setLayout(top_layout)

        return self

    def init_event(self):
        self.search_push_button.clicked.connect(self.search)
        self.search_content_text_list.itemClicked.connect(self.copy_text)

    def search(self):
        # 查询状态
        self.tip_label.setText(self.tr("正在查询请稍后..."))
        # 搜索的电影名称 (用户输入)
        movie_name = self.movie_name_line_edit.text()
        if movie_name:
            # 资源网站单一
            self.work.render(movie_name, self.tip_label, self.search_content_text_list )
            # 多个资源网站配置
            # self.work.render(movie_name, self.movie_source_combobox,
            #                  self.tip_label, self.search_content_text_list)
        else:
            self.critical("请输入电影名称!")

    # 电影名称不得为空
    def critical(self, message):
        """
        when the movieName is None,
        remind users
        """
        QMessageBox.critical(self, self.tr("温馨提示"),
                             self.tr(message))

    def copy_text(self):
        copied_text = self.search_content_text_list.currentItem().text()
        QApplication.clipboard().clear()
        QApplication.clipboard().setText(copied_text)
        self.slot_information()

    def slot_information(self):
        QMessageBox.information(self, "Success!", self.tr("成功将内容复制到剪贴板上!"))

# 查询过程
class WorkThread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def render(self, movie_name, tip_label, search_content_text_list):
        self.movies_list = []
        # self.movie_source_combobox = movie_source_combobox
        self.movie_name = movie_name
        self.tip_label = tip_label
        self.search_content_text_list = search_content_text_list
        self.start()

    def get_select_movie_source(self, movie_name):
        movies, url, params = None, None, {
            "kwtype": "0", "searchtype": "title"}
        select_source = self.movie_source_combobox.currentText()
        if select_source == self.tr('电影天堂'):
            # movies = MovieHeaven()
            url = "http://s.dydytt.net/plus/search.php"
            params["keyword"] = movie_name.encode('gb2312')
        return movie_name


    def run(self):
        try:
            self.movies_list = search_movie(self.movie_name)
            print(self.movies_list)
        except Exception as e:
            self.movies_list.append(self.tr("访问错误，请联系管理员。"))
        finally:
            self.search_content_text_list.clear()
            self.search_content_text_list.addItems(self.movies_list)
            self.tip_label.setText(self.tr("查询结束"))


app = QApplication(sys.argv)
dialog = LayoutDialog()
dialog.show()
app.exec_()

