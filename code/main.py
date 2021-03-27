import os
from PyQt5 import uic
from PyQt5 import *

from PyQt5.QtGui import QPixmap
from PySide2.QtWidgets import *
import pr
class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = uic.loadUi("./../ui/homework.ui")
        pixmap = QPixmap("/home/starfish/桌面/python_project/spider/2021-02-17.jpg")  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        self.ui.pic_show.setPixmap(pixmap)  # 在label上显示图片
        self.ui.pic_show.setScaledContents(True)
        self.ui.file.clicked.connect(self.show_text)
        self.ui.to_left.clicked.connect(self.to_left)
        self.ui.to_right.clicked.connect(self.to_right)
        self.ui.to_up.clicked.connect(self.to_up)
        self.ui.to_down.clicked.connect(self.to_down)
        self.ui.pick_color.clicked.connect(self.pick_color)
        print(type(self))
        print(type(self.ui))

    def to_left(self):
        x = self.ui.preview_text.pos().x()
        y = self.ui.preview_text.pos().y()
        self.ui.preview_text.move(x - 1, y)


    def to_right(self):
        x = self.ui.preview_text.pos().x()
        y = self.ui.preview_text.pos().y()
        self.ui.preview_text.move(x + 1, y)

    def to_up(self):
        x = self.ui.preview_text.pos().x()
        y = self.ui.preview_text.pos().y()
        self.ui.preview_text.move(x, y - 1)

    def to_down(self):
        x = self.ui.preview_text.pos().x()
        y = self.ui.preview_text.pos().y()
        self.ui.preview_text.move(x, y + 1)

    def show_text(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName()  #直接不写任何参数
        a=pr.split_sentence(fileName_choose)
        with open(a,'r')as f:
            content=f.read()
        self.ui.text_edit.setText(content)
    def pick_color(self):
        color = QColorDialog.getColor()
        print(color)
        return color
app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()

