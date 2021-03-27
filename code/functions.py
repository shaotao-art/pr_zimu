
from PySide2.QtWidgets import *

def to_left(self):
    x = self.preview_text.pos().x()
    y = self.preview_text.pos().y()
    self.preview_text.move(x - 1, y)


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
    # QFileDialog.getOpenFileName(self.ui, "选择你要上传的文档", self.cwd, "图片类型 (*.txt)")
    fileName_choose, filetype = QFileDialog.getOpenFileName(self)  # 设置文件扩展名过滤,用双分号间隔

    if fileName_choose == "":
        print("\n取消选择")
        return

    print("\n你选择的文件为:")
    print(fileName_choose)
    print("文件筛选器类型: ", filetype)