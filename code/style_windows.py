import PyQt4.uic
from PyQt4 import QtGui
from PyQt4.QtGui import QPixmap



class style_window:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = PyQt4.uic.loadUi("./../ui/style_window.ui")

        img = QPixmap("./../media/one_frame.png")
        self.ui.pic_show.setPixmap(img)
        self.ui.pic_show.setScaledContents(True)

        # 文本框移动函数
        self.ui.to_left.clicked.connect(self.to_left)
        self.ui.to_right.clicked.connect(self.to_right)
        self.ui.to_up.clicked.connect(self.to_up)
        self.ui.to_down.clicked.connect(self.to_down)

        #颜色与字体选择函数
        self.ui.pick_color.clicked.connect(self.pick_color)
        self.ui.pick_font.clicked.connect(self.pick_font)

        #默认样式表
        self.font = {
            'font-family': 'Arial',  # 字体
            'font-style': '',  # 斜体 italic
            'font-weight': '',  # 粗细 blod
            'font-size': 50,  # 字体大小 9px
            'text-decoration': '',  # 删除线 下划线 line-through underline
            'color': [255, 255, 255]  # rgb(0,0,0)
        }
        self.change_style_in_preview_text()

    #移动文本框
    def to_left(self):
        x = self.ui.preview_text.pos().x()
        y = self.ui.preview_text.pos().y()
        self.ui.preview_text.move(x - 5, y)

    def to_right(self):
        x = self.ui.preview_text.pos().x()
        y = self.ui.preview_text.pos().y()
        self.ui.preview_text.move(x + 5, y)

    def to_up(self):
        x = self.ui.preview_text.pos().x()
        y = self.ui.preview_text.pos().y()
        self.ui.preview_text.move(x, y - 5)

    def to_down(self):
        x = self.ui.preview_text.pos().x()
        y = self.ui.preview_text.pos().y()
        self.ui.preview_text.move(x, y + 5)


    #颜色选择
    def pick_color(self):
        color = QtGui.QColorDialog.getColor()
        self.font['color'][0]=color.red()
        self.font['color'][1] = color.green()
        self.font['color'][2] = color.blue()
        self.change_style_in_preview_text()
        return color.red(),color.green(),color.blue()   #RGB


    def pick_font(self):
        font,ok=QtGui.QFontDialog.getFont()
        # 字体
        self.font['font-family']=font.family()
        #加粗
        if font.bold():
            self.font['font-weight'] = 'bold'
        #斜体
        if font.italic():
            self.font['font-style'] = 'italic'

        self.font['font-size'] = int(font.pointSizeF())
        #删除线 下划线
        if font.strikeOut() and font.underline():
            self.font['text-decoration']="line-through underline"
        elif font.strikeOut()==1 and font.underline()==0:
            self.font['text-decoration']='line-through'
        elif font.strikeOut()==0 and font.underline()==1:
            self.font['text-decoration']= 'underline'
        else:
            pass
        self.change_style_in_preview_text()
        #字体 加粗 斜体 字号 删除线 下划线   (该版本qt中font—weight 无效)
        return font.family() ,font.bold(),font.italic(),font.pointSizeF(),font.strikeOut(),font.underline()

    #点击主窗口的PB 来显示该窗口
    def show(self):
        self.ui.show()



    # 根据self.font来改变文本框中文本的样式
    def change_style_in_preview_text(self):
        #处理self.font文本
        style_sheet=''
        for k, v in self.font.items():
            if v != '':
                if k == 'font-size':
                    style_sheet += (str(k) + ':' + str(v) + 'px;')
                elif k == 'color':
                    style_sheet += (str(k) + ':' + f'rgb({v[0]},{v[1]},{v[2]})')
                else:
                    style_sheet += (str(k) + ':' + str(v) + ';')
        self.ui.preview_text.setStyleSheet(style_sheet)


if __name__ =="__main__":
    app = QtGui.QApplication([])
    main_window = style_window()
    main_window.ui.show()
    app.exec_()