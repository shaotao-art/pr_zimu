
from PyQt4 import phonon
import PyQt4.uic
from PyQt4 import QtCore, QtGui
import pandas as pd
import numpy as np
import other_func
import little_func
import style_windows

class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = PyQt4.uic.loadUi("./../ui/homework.ui")
        self.video_path=None
        self.ui.choose_txt.clicked.connect(self.show_text)
        self.ui.choose_video.clicked.connect(self.select_video)

        self.ui.play_or_pause_PB.clicked.connect(self.paly_or_pause)


        #表格显示相关
        self.ui.tableWidget.setColumnWidth(0, 300)
        self.ui.tableWidget.setColumnWidth(1, 300)
        self.ui.tableWidget.setColumnWidth(2, 1550)
        self.ui.tableWidget.setRowCount(10)
        self.ui.tableWidget.setColumnCount(3)


        self.ui.recode_time.clicked.connect(self.recode_time_point)
        self.ui.delete_time.clicked.connect(self.delete_time_point)

        #时间节点记录相关
        self.num_data = np.zeros([10,2],dtype=np.int64)


        self.current_clo1 = 0


    def recode_time_point(self):

        print(self.current_clo1)
        #获得当前时间点
        point=self.ui.videoPlayer.currentTime()#ms单位
        time=little_func.modify_to_s(point)
        #添加到num_data数据中
        self.num_data[self.current_clo1][1]=point

        self.ui.tableWidget.setItem(self.current_clo1, 1, QtGui.QTableWidgetItem(time))

        self.current_clo1 += 1


        #上一个结束节点  就是  下一个的开始节点
        self.num_data[self.current_clo1][0] = point
        self.ui.tableWidget.setItem(self.current_clo1, 0, QtGui.QTableWidgetItem(time))




    def delete_time_point(self):
        # 删除num_data中数据
        self.num_data[self.current_clo1][0] = 0
        self.ui.tableWidget.setItem(self.current_clo1, 0, QtGui.QTableWidgetItem(str('')))
        self.current_clo1 -= 1
        self.num_data[self.current_clo1][1] = 0
        self.ui.tableWidget.setItem(self.current_clo1, 1, QtGui.QTableWidgetItem(str('')))





    def paly_or_pause(self):
        if self.ui.videoPlayer.isPlaying():
            self.ui.videoPlayer.pause()
        elif self.ui.videoPlayer.isPaused():
            self.ui.videoPlayer.play()
        else:
            self.ui.videoPlayer.play()


    def show_text(self):
        fileName_choose= QtGui.QFileDialog.getOpenFileName(self.ui, 'Open file', './')
        a=other_func.split_sentence(fileName_choose)
        with open(a,'r',encoding='utf-8')as f:
            content=f.readlines()

        rows=len(content)
        self.num_data=np.ndarray([rows,3])
        self.ui.tableWidget.setRowCount(rows)
        for i in range(0,rows):
            self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(content[i]))



    def select_video(self):
        video_filepath = QtGui.QFileDialog.getOpenFileName()
        self.video_path=video_filepath
        print(self.video_path)
        self.play_video(video_filepath)

    def play_video(self,filepath):
        self.ui.videoPlayer.show()
        media = phonon.Phonon.MediaSource(filepath)
        self.ui.videoPlayer.load(media)
        self.ui.seekSlider.setMediaObject(self.ui.videoPlayer.mediaObject())
        self.ui.volumeSlider.setAudioOutput(self.ui.videoPlayer.audioOutput())
        self.ui.videoPlayer.play()

    #生成.srt文件
    def convert_to_srt(self):
        #获取表格中的数据（读取numpy数组中数据）  以及字幕的数据
        with open('./../docs/done.txt','r')as f:
            lines=f.readlines()
        #字符串按照srt文本形式格式化并写入
        with open ("zimu.srt",'w')as f:
            for i in range(0,len(lines)):
                time=f'{self.num_data[i][0]} -->{self.num_data[i][1]}'
                str_to_write=str(i)+'\n'+time+'\n'+lines[i]+'\n'
                f.write(str_to_write)

if __name__ =="__main__":
    app = QtGui.QApplication([])
    main_window = Stats()
    style_window=style_windows.style_window()
    main_window.ui.style_PB.clicked.connect(style_window.show)
    main_window.ui.show()
    app.exec_()