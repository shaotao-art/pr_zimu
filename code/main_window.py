from PyQt4 import phonon
import PyQt4.uic
from PyQt4 import  QtGui
import numpy as np
from make_srt import modify_to_s
import style_windows
from other_func import split_sentence
import combine_video
import translate


class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = PyQt4.uic.loadUi("./../ui/homework.ui")
        self.ui.choose_txt.clicked.connect(self.show_text)
        self.ui.choose_video.clicked.connect(self.select_video)

        self.ui.play_or_pause_PB.clicked.connect(self.paly_or_pause)

        #英文爬虫翻译
        self.ui.english_PB.clicked.connect(self.translate)

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


        self.current_position_in_table = 0
        # video_info :width, height, frame_nums, framerate
        self.video_info=[]
        # video路径
        self.video_path=''

        #子窗口展示相关
        self.style_window = style_windows.style_window()
        self.ui.style_PB.clicked.connect(self.show_style_window)

    def show_style_window(self):
        self.style_window.show()

    def translate(self):
        #获得分行后的文本
        lines=combine_video.read_lines()
        with open('./../docs/translate_done.txt','w',encoding='utf-8')as f:
            for each in lines:
                if translate.get_res(each) is not None:
                    f.write(translate.get_res(each)+'\n')
                else:
                    print('something is wrong')
        print('translation done')



    def recode_time_point(self):
        #应检查当前是否有视频  没有视频的话 current time总是0

        #获得当前时间点
        point=self.ui.videoPlayer.currentTime()#ms单位
        time=modify_to_s(point)

        #计算当前时间点的row col
        row=int(self.current_position_in_table/2)
        col=self.current_position_in_table%2
        print(self.current_position_in_table,row,col)

        # 添加到num_data数据中
        self.ui.tableWidget.setItem(row, col, QtGui.QTableWidgetItem(time))
        #更新 current_position_in_table
        self.current_position_in_table+=1



    def delete_time_point(self):
        # 计算当前时间点的row col
        row = int(self.current_position_in_table / 2)
        col = self.current_position_in_table % 2
        self.ui.tableWidget.setItem(row, col, QtGui.QTableWidgetItem(str('')))

        #应检查是否为空  能否继续删除
        if self.current_position_in_table>=1:
            self.current_position_in_table-=1





    def paly_or_pause(self):
        if self.ui.videoPlayer.isPlaying():
            self.ui.videoPlayer.pause()
        elif self.ui.videoPlayer.isPaused():
            self.ui.videoPlayer.play()
        else:
            self.ui.videoPlayer.play()


    def show_text(self):
        fileName_choose= QtGui.QFileDialog.getOpenFileName(self.ui, 'Open file', './')
        split_sentence(fileName_choose)
        with open('./../docs/done.txt','r',encoding='utf-8')as f:
            content=f.readlines()

        rows=len(content)
        self.num_data=np.ndarray([rows,3])
        self.ui.tableWidget.setRowCount(rows)
        for i in range(0,rows):
            self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(content[i]))



    def select_video(self):
        video_filepath = QtGui.QFileDialog.getOpenFileName()
        self.video_path=video_filepath

        # 此时会有一个多线程的问题
        # get_audio 应建立一个新线程在后台运行
        self.play_video(video_filepath)
        #分离音频
        combine_video.get_audio(video_filepath)
        #读取视频信息 并存下一帧的图片
        self.video_info=combine_video.get_video_info(video_filepath)


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


    main_window.ui.show()
    app.exec_()