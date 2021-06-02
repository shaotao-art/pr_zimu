import PyQt5.uic
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFontDialog,QColorDialog


class style_window:
    def __init__(self,style_dic):
        # 从文件中加载UI定义
        self.ui = PyQt5.uic.loadUi("./../ui/style_window.ui")



        # # 文本框移动函数
        # self.ui.to_left.clicked.connect(self.to_left)
        # self.ui.to_right.clicked.connect(self.to_right)
        # self.ui.to_up.clicked.connect(self.to_up)
        # self.ui.to_down.clicked.connect(self.to_down)

        #颜色与字体选择函数
        self.ui.pick_color.clicked.connect(self.pick_color)
        self.ui.pick_font.clicked.connect(self.pick_font)


        '''
        	font-size: 60px ;
            text-decoration:underline  line-through;
            font: bold italic large "Times New Roman"

        '''
        self.style_dic=style_dic
        self.style_dic['font']=['"Arial"']
        self.style_dic['font-size'] =72
        self.style_dic['text-decoration'] = []
        self.style_dic['color'] = [255,255,255,None]
        self.change_style_in_preview_text()

    # #移动文本框
    # def to_left(self):
    #     x = self.ui.preview_text.pos().x()
    #     y = self.ui.preview_text.pos().y()
    #     self.ui.preview_text.move(x - 5, y)
    #
    # def to_right(self):
    #     x = self.ui.preview_text.pos().x()
    #     y = self.ui.preview_text.pos().y()
    #     self.ui.preview_text.move(x + 5, y)
    #
    # def to_up(self):
    #     x = self.ui.preview_text.pos().x()
    #     y = self.ui.preview_text.pos().y()
    #     self.ui.preview_text.move(x, y - 5)
    #
    # def to_down(self):
    #     x = self.ui.preview_text.pos().x()
    #     y = self.ui.preview_text.pos().y()
    #     self.ui.preview_text.move(x, y + 5)


    #颜色选择
    def pick_color(self):
        color = QColorDialog.getColor()
        self.style_dic['color'][0]=color.red()
        self.style_dic['color'][1] = color.green()
        self.style_dic['color'][2] = color.blue()
        self.change_style_in_preview_text()
        self.style_dic[3]=color.name()
        return color.name()


    def pick_font(self):
        font,ok=QFontDialog.getFont()
        self.style_dic['font'].clear()
        #加粗
        if font.bold():
            self.style_dic['font'].append('bold')
        #斜体
        if font.italic():
            self.style_dic['font'] .append('italic')
        # 字体
        self.style_dic['font'].append(str('"'+font.family()+'"'))

        self.style_dic['font-size'] = int(font.pointSizeF())
        #删除线 下划线
        if font.strikeOut() and font.underline():
            self.style_dic['text-decoration']="line-through underline"
        elif font.strikeOut()==1 and font.underline()==0:
            self.style_dic['text-decoration']='line-through'
        elif font.strikeOut()==0 and font.underline()==1:
            self.style_dic['text-decoration']= 'underline'
        else:
            self.style_dic['text-decoration']= ''
        self.change_style_in_preview_text()

        return font.family() ,font.bold(),font.italic(),font.pointSizeF(),font.strikeOut(),font.underline()

    #点击主窗口的PB 来显示该窗口
    def show(self):
        img = QPixmap("./../temp/one_frame.png")
        self.ui.pic_show.setPixmap(img)
        self.ui.pic_show.setScaledContents(True)
        self.ui.show()



    # 根据self.font来改变文本框中文本的样式
    def change_style_in_preview_text(self):
        # print(self.style_dic)
        #处理self.font文本
        style_sheet=''
        for k, v in self.style_dic.items():
            if v != '':
                if k == 'font':
                    style_sheet += str(k) + ':'
                    for each in v:
                        style_sheet +=str(each)+' '
                    style_sheet+=';'
                elif k == 'color':
                    style_sheet += (str(k) + ':' + f'rgb({v[0]},{v[1]},{v[2]});')
                elif k=='font-size':
                    style_sheet += (str(k) + ':' + str(v)+'px' + ';')
                elif k=='text-decoration':
                    style_sheet += (str(k) + ':' + str(v) + ';')
        # print(style_sheet)
        self.ui.preview_text.setStyleSheet(style_sheet)


if __name__ =="__main__":
    app = QtGui.QApplication([])
    main_window = style_window()
    main_window.ui.show()
    app.exec_()