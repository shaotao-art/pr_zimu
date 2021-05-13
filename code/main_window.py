from PyQt4 import phonon,QtGui
import PyQt4.uic
import numpy as np
from make_srt import modify_to_s ,make_srt,modify_to_s_in_auto
import style_windows
from other_func import split_sentence
import combine_video
import translate
import threading
from PyQt4.QtGui import *
# import handle_audio

class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = PyQt4.uic.loadUi("./../ui/main_windows.ui")

        #选择字幕文本文件按钮
        self.ui.choose_txt.clicked.connect(self.select_text)

        #选择视频按钮
        self.ui.choose_video.clicked.connect(self.select_video)

        #视频播放按钮
        self.ui.play_or_pause_PB.clicked.connect(self.paly_or_pause)

        #英文爬虫翻译
        self.ui.english_PB.clicked.connect(self.translate)

        #设置显示文本表格的高和宽
        self.ui.tableWidget.setColumnWidth(0, 300)
        self.ui.tableWidget.setColumnWidth(1, 300)
        self.ui.tableWidget.setColumnWidth(2, 1550)
        self.ui.tableWidget.setRowCount(20)
        self.ui.tableWidget.setColumnCount(3)

        #生成.srt文件
        self.ui.make_srt.clicked.connect(self.convert_to_srt)

        #添加时间点 与 删除时间点按钮
        self.ui.recode_time.clicked.connect(self.recode_time_point)
        self.ui.delete_time.clicked.connect(self.delete_time_point)


        #添加删除时间点的计数
        self.current_position_in_table = -1


        # video_info :width, height, frame_nums, framerate
        self.video_info=[]
        # video路径
        self.video_path=''
        #audio 路径
        self.audio_path=''
        #文本文件路径
        self.text_path=''


        # 从子窗口获得样式表
        self.stylesheet = dict()

        #子窗口展示相关
        self.style_window = style_windows.style_window(self.stylesheet)
        self.ui.style_PB.clicked.connect(self.style_window.show)


        # 将字幕文本直接写到字幕的每一帧里去
        self.ui.output_hard_zimu.clicked.connect(self.make_hard_zimu)


        #自动定位时间点
        self.ui.auto_detect_time_point.clicked.connect(self.auto_detect_time_point)



        #**********************************************************************************************
        #测试用

        # video路径
        self.video_path='./../media/test_video.mp4'

        #文本文件路径
        self.text_path='./../docs/2.txt'

        self.audio_path = './../test_audio/录音-002.wav'

        self.after_select_text()
        self.after_select_video()

        self.msg_box=QMessageBox()
        self.msg_box.setText("提醒：")
        self.msg_box.setWindowTitle("MessageBox")
        self.msg_box.setStandardButtons(QMessageBox.Ok )

        self.ui.recode.clicked.connect(self.recode)

        #存储时间节点的numpy数组

        time_points=[[ 8978,13879],
                     [13879,18987],
                     [18987,20099],
                     [20099,24556],
                     [24556,27860],
                     [27860,29761],
                     [29761,31423],
                     [31423,35228],
                     [35228,38395],
                     [38395,41105],
                     [41105,43045],
                     [43045,45255],
                     [45255,47570],
                     [47570,51692],
                     [51692,55933],
                     [55933,57314],
                     [57314,58429],
                     [58429,59497],
                     [59497,60583],
                     [60583,62593],
                     [62593,64697],
                     [64697,66329],
                     [66329,71039],
                     [71039,72867],
                     [72867,75112],
                     [75112,76281],
                     [76281,77981],
                     [77981,79806],
                     [79806,81625],
                     [81625,83064],
                     [83064,84761],
                     [84761,87047],
                     [87047,90227]]
        self.num_data = np.asarray(time_points)

        #最终结果 时间点列表
        self.time_lst=[[],[]]


        self.ui.printnum_data.clicked.connect(self.print_numdata)

    def show_msg_box(self,msg):
        self.msg_box.setInformativeText(msg)
        self.msg_box.show()
    def print_numdata(self):
        print(self.num_data)
        print(self.stylesheet)






    def make_hard_zimu(self):
        # video_info :width, height, frame_nums, framerate
        lines=combine_video.read_lines('./../docs/done.txt')
        combine_video.put_text_on_each_frame(framerate=self.video_info[3],
                                             frame_num=self.video_info[2],
                                             width=self.video_info[0],
                                             height=self.video_info[1],
                                             num_data=self.num_data,
                                             text=lines,
                                             to_bottem=90,
                                             input_video_path=self.video_path)
        combine_video.combine_audio_video(output_path='./../media/final_video.mp4')



    def translate(self):
        #获得分行后的文本
        lines=combine_video.read_lines('./../docs/done.txt')



        with open('./../docs/translate_done.txt','w',encoding='utf-8')as f:
            for each in lines:
                if translate.get_res(each) is not None:
                    f.write(translate.get_res(each)+'\n')
                else:
                    print('something in tranlation is wrong')
        print('translation done')

    def recode(self):
        #获得当前选中的表格
        row=self.ui.tableWidget.currentRow()
        col=self.ui.tableWidget.currentColumn()
        #写入文本

        # 获得当前时间点
        point = self.ui.videoPlayer.currentTime()  # ms单位

        # 格式为 f'{hour}:{minute}:{second},{ms}'
        time = modify_to_s(point)

        # 设置表格数据

        self.ui.tableWidget.setItem(row, col, QtGui.QTableWidgetItem(time))



    def recode_time_point(self):
        #应检查当前是否有视频  没有视频的话 current time总是0
        if self.video_path!='':
            # 更新 current_position_in_table
            self.current_position_in_table += 1

            #获得当前时间点
            point=self.ui.videoPlayer.currentTime()#ms单位

            #格式为 f'{hour}:{minute}:{second},{ms}'
            time=modify_to_s(point)

            #计算当前时间点的row col
            row=int(self.current_position_in_table/2)
            col=self.current_position_in_table%2


            # 设置表格数据

            self.ui.tableWidget.setItem(row, col, QtGui.QTableWidgetItem(time))

        else:
            pass


    def delete_time_point(self):
        # 计算当前时间点的row col
        row = int(self.current_position_in_table / 2)
        col = self.current_position_in_table % 2
        #更新表格
        self.ui.tableWidget.setItem(row, col, QtGui.QTableWidgetItem(str('')))

        #应检查是否为空  能否继续删除
        if self.current_position_in_table>=0:
            self.current_position_in_table-=1
        else:
            pass




    #视频的播放与暂停
    def paly_or_pause(self):
        if self.ui.videoPlayer.isPlaying():
            self.ui.videoPlayer.pause()
        elif self.ui.videoPlayer.isPaused():
            self.ui.videoPlayer.play()
        else:
            self.ui.videoPlayer.play()

    #将文本文件显示在表格中
    def select_text(self):
        #用户选择文本文件
        self.text_path= QtGui.QFileDialog.getOpenFileName(self.ui, 'Open file', './')
        self.after_select_video()

    def after_select_text(self):
        #文本文件分行并存储
        split_sentence(self.text_path)

        #读取分行后的文件
        content=combine_video.read_lines('./../docs/done.txt')


        rows = len(content)

        #根据文章的长度初始化numpy 数组
        self.num_data=np.zeros(shape=[rows,2],dtype=np.int64)
        self.ui.tableWidget.setRowCount(rows)

        # 给每个单元格设置QTableWidgetItem
        for i in range(0,rows):
            for j in range(0,2):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(''))

        #在表格中显示文本
        for i in range(0,rows):
            self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(content[i]))


    #视频选择
    def select_video(self):
        video_filepath = QtGui.QFileDialog.getOpenFileName()
        self.video_path=video_filepath
        self.after_select_video()

    def after_select_video(self):
        # 此时会有一个多线程的问题
        # get_audio 应建立一个新线程在后台运行
        self.play_video(self.video_path)
        self.video_info=combine_video.get_video_info(self.video_path)

        #分离音频
        #创建新线程
        thread_audio=threading.Thread(target=combine_video.get_audio,
                                      args=(self.video_path,))

        #开始新线程
        thread_audio.start()




    #播放视频
    def play_video(self,filepath):
        self.ui.videoPlayer.show()
        media = phonon.Phonon.MediaSource(filepath)
        self.ui.videoPlayer.load(media)
        self.ui.seekSlider.setMediaObject(self.ui.videoPlayer.mediaObject())
        self.ui.volumeSlider.setAudioOutput(self.ui.videoPlayer.audioOutput())
        self.ui.videoPlayer.play()

    #生成.srt文件
    def convert_to_srt(self):
        #获取表格中的内容来填充time_point_lst
        for i in range(0,self.ui.tableWidget.rowCount()):
            if self.ui.tableWidget.item(i,0) is not None and self.ui.tableWidget.item(i,1) is not None:
                self.time_lst[0][i]=(self.ui.tableWidget.item(i,0).text())
                self.time_lst[1][i]=(self.ui.tableWidget.item(i, 1).text())
            else:
                pass
        with open('./../docs/final_in_table.txt','w')as f:
            for i in range(0, self.ui.tableWidget.rowCount()):
                if self.ui.tableWidget.item(i, 0) is not None:
                    f.write(self.ui.tableWidget.item(i,2).text())
                else:
                    pass
        res=make_srt(self.time_lst,'./../docs/2.txt')
        if res==1:
            print('******  make_srt  check! ')
        if res==0:
            print('******  something goes wrong in make_srt! ')


    def auto_detect_time_point(self):
        #运行函数
        audio = handle_audio.audio_analysis(audio_path=self.audio_path, text_path=self.text_path)

        self.time_lst[0],self.time_lst[1]=audio.run()


        modify_to_s_in_auto(self.time_lst)


        #将数据写到表格中
        for i in range(0,self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.item(i,0).setText(str(self.time_lst[0][i]))
            self.ui.tableWidget.item(i, 1).setText(str(self.time_lst[1][i]))




if __name__ =="__main__":
    app = QtGui.QApplication([])
    main_window = Stats()
    main_window.ui.show()
    app.exec_()
