from PyQt4 import phonon
import PyQt4.uic
from PyQt4 import  QtGui
import numpy as np
from make_srt import modify_to_s
import style_windows
from other_func import split_sentence
import combine_video
import translate
import threading

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



        self.current_position_in_table = -1
        # video_info :width, height, frame_nums, framerate
        self.video_info=[]
        # video路径
        self.video_path=''

        #子窗口展示相关
        self.style_window = style_windows.style_window()
        self.ui.style_PB.clicked.connect(self.style_window.show)

        # self.style_window.ui.closed.connect(self.get_stylesheet)


        #从子窗口获得的样式表
        self.stylesheet=None

        # 将字幕文本直接写到字幕的每一帧里去
        self.ui.output_hard_zimu.clicked.connect(self.make_hard_zimu)

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

        self.ui.printnum_data.clicked.connect(self.print_numdata)

    def print_numdata(self):
        print(self.num_data)


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


    def get_stylesheet(self):
        self.stylesheet=self.style_window.font
        print('i am right')

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

        # 更新 current_position_in_table
        self.current_position_in_table += 1

        #获得当前时间点
        point=self.ui.videoPlayer.currentTime()#ms单位
        time=modify_to_s(point)

        #计算当前时间点的row col
        row=int(self.current_position_in_table/2)
        col=self.current_position_in_table%2


        # 添加到num_data数据中 并设置表格数据
        self.num_data[row][col]=point
        self.ui.tableWidget.setItem(row, col, QtGui.QTableWidgetItem(time))




    def delete_time_point(self):
        # 计算当前时间点的row col
        row = int(self.current_position_in_table / 2)
        col = self.current_position_in_table % 2
        #更新表格 以及 numdata数据
        self.ui.tableWidget.setItem(row, col, QtGui.QTableWidgetItem(str('')))
        self.num_data[row][col]=0
        #应检查是否为空  能否继续删除

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

        rows = len(content)

        #根据文章的长度初始化numpy 数组
        self.num_data=np.zeros(shape=[rows,2],dtype=np.int64)



        self.ui.tableWidget.setRowCount(rows)
        for i in range(0,rows):
            self.ui.tableWidget.setItem(i, 2, QtGui.QTableWidgetItem(content[i]))



    def select_video(self):
        video_filepath = QtGui.QFileDialog.getOpenFileName()
        self.video_path=video_filepath

        # 此时会有一个多线程的问题
        # get_audio 应建立一个新线程在后台运行
        self.play_video(video_filepath)

        self.video_info=combine_video.get_video_info(video_filepath)
        #分离音频
        #创建新线程
        thread_audio=threading.Thread(target=combine_video.get_audio,
                                      args=(video_filepath,))

        #开始新线程
        thread_audio.start()





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
