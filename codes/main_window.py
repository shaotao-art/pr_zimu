import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtMultimedia,QtCore

import make_hard_zimu

from make_srt import modify_to_s ,make_srt,modify_to_s_in_auto,make_srt_eng
import style_windows
from other_func import split_sentence,read_lines
import combine_video
import translate
import threading
import make_ass
import handle_audio

class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = uic.loadUi("./../ui/main_windows.ui")

        #选择字幕文本文件按钮
        self.ui.choose_txt.clicked.connect(self.select_text)

        #选择视频按钮
        self.ui.choose_video.clicked.connect(self.select_video)

        #视频播放按钮
        self.ui.play_or_pause_PB.clicked.connect(self.paly_or_pause)

        #视频组件
        self.player = QtMultimedia.QMediaPlayer(None, QtMultimedia.QMediaPlayer.VideoSurface)
        self.player.setVideoOutput(self.ui.videoPlayer)

        #设置显示文本表格的高和宽
        self.ui.tableWidget.setColumnWidth(0, 200)
        self.ui.tableWidget.setColumnWidth(1, 200)
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(20)
        self.ui.tableWidget.setRowCount(20)
        self.ui.tableWidget.setColumnCount(3)

        #生成.srt文件
        self.ui.make_srt.clicked.connect(self.make_srt)

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

        self.srt_path=''

        #自动确定时间点时手动添加时间点
        self.ui.recode.clicked.connect(self.recode)

        # 从子窗口获得样式表
        self.stylesheet = dict()

        #子窗口展示相关
        self.style_window = style_windows.style_window(self.stylesheet)
        self.ui.style_PB.clicked.connect(self.style_window.show)


        # 将字幕文本直接写到字幕的每一帧里去
        self.ui.output_hard_zimu.clicked.connect(self.make_hard_zimu)


        #自动定位时间点
        self.ui.auto_detect_time_point.clicked.connect(self.auto_detect_time_point)


        #最终结果 时间点列表
        self.time_lst=[[],[]]

        #保存当前工程
        self.ui.save.clicked.connect(self.save)

        #打开已有工程
        self.ui.open_old.clicked.connect(self.open_proj)

        #生成.ass文件
        self.ui.make_ass.clicked.connect(self.make_ass)

        self.player.durationChanged.connect(self.getDuration)
        self.player.positionChanged.connect(self.getPosition)
        self.ui.sld_duration.sliderMoved.connect(self.updatePosition)

        #标志已经翻译过文本
        self.have_translated_flag=0

    #视频展示相关
    def getDuration(self, d):
        '''d 为时间总长( ms)'''
        self.ui.sld_duration.setRange(0, d)
        self.ui.sld_duration.setEnabled(True)
        self.displayTime(d)

    def getPosition(self, p):
        self.ui.sld_duration.setValue(p)
        self.displayTime(self.ui.sld_duration.maximum()-p)
    # 显示剩余时间
    def displayTime(self, ms):
        minutes = int(ms/60000)
        seconds = int((ms-minutes*60000)/1000)
        self.ui.lab_duration.setText('{}:{}'.format(minutes, seconds))
    # 更新进度条
    def updatePosition(self, v):
        self.player.setPosition(v)
        self.displayTime(self.ui.sld_duration.maximum()-v)

    def open_proj(self):
        #选择工程文件
        proj_path = QFileDialog.getOpenFileName(self.ui, 'Open file', './../projs')[0]
        if proj_path!='':
            with open(proj_path, 'r', encoding='utf-8')as f:
                text=str(f.read())
            lst=text.split('*')

            #获取视频信息
            self.video_path=lst[0]
            self.text_path = lst[1]
            self.after_select_text(flag=1)
            self.after_select_video(flag=1)
            #在表格中设置数据
            for i in range(0,int((len(lst)-2)/2)):
                row=i/2
                col=i%2
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(lst[i+2])))
            #获取表格中的内容来填充time_point_lst
            for i in range(0, self.ui.tableWidget.rowCount()):
                self.time_lst[0].append(self.ui.tableWidget.item(i, 0).text())
                self.time_lst[1].append(self.ui.tableWidget.item(i, 1).text())



    def save(self):
        save_path = QFileDialog.getSaveFileName(self.ui, 'save file', './../projs', '.zimu')[0]
        if save_path!='':
            # 获取表格中的内容来填充time_point_lst
            for i in range(0, self.ui.tableWidget.rowCount()):
                self.time_lst[0].append(self.ui.tableWidget.item(i, 0).text())
                self.time_lst[1].append(self.ui.tableWidget.item(i, 1).text())
            #将当前信息写入
            with open(save_path+'.zimu', 'w', encoding='utf-8')as f:
                f.write(self.video_path + '*' + self.text_path + '*')
                for i in range(0, len(self.time_lst[0])):
                    f.write(self.time_lst[0][i] + '*' + self.time_lst[1][i] + '*')
            QMessageBox.information(
                self.ui,
                '提示',
                '工程文件保存成功！',
            )




    #单独录入时间点
    def recode(self):
        if self.video_path != '':
            #获得当前选中的表格
            row=self.ui.tableWidget.currentRow()
            col=self.ui.tableWidget.currentColumn()
            #写入文本

            # 获得当前时间点
            point = self.player.position()  # ms单位

            # 格式为 f'{hour}:{minute}:{second},{ms}'
            time = modify_to_s(point)

            # 设置表格数据

            self.ui.tableWidget.setItem(row, col, QTableWidgetItem(time))

        else:
            QMessageBox.warning(
                self.ui,
                'window',
                '请导入视频')

    #按顺序录入时间点
    def recode_time_point(self):
        #应检查当前是否有视频  没有视频的话 current time总是0
        if self.video_path!='':
            # 更新 current_position_in_table
            self.current_position_in_table += 1

            #获得当前时间点
            point=self.player.position()#ms单位

            #格式为 f'{hour}:{minute}:{second},{ms}'
            time=modify_to_s(point)

            #计算当前时间点的row col
            row=int(self.current_position_in_table/2)
            col=self.current_position_in_table%2


            # 设置表格数据

            self.ui.tableWidget.setItem(row, col,QTableWidgetItem(time))
        else:
            QMessageBox.warning(
                self.ui,
                'window',
                '请导入视频')


    def delete_time_point(self):
        # 计算当前时间点的row col
        row = int(self.current_position_in_table / 2)
        col = self.current_position_in_table % 2
        #更新表格
        self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str('')))

        #应检查是否为空  能否继续删除
        if self.current_position_in_table>=0:
            self.current_position_in_table-=1





    #视频的播放与暂停
    def paly_or_pause(self):
        if self.player.state() == 1:
            self.player.pause()
        else:
            self.player.play()
    #将文本文件显示在表格中
    def select_text(self):
        #用户选择文本文件
        self.text_path= QFileDialog.getOpenFileName(self.ui, 'Open file', './../test_docs')[0]
        if self.text_path!='':
            self.after_select_text()

    #flag为0 是第一次打开   为1 是通过打开工程文件打开  所以一些工作不必做
    def after_select_text(self,flag=0):
        if flag==0:
            #文本文件分行并存储
            split_sentence(self.text_path)

        #读取分行后的文件
        content=read_lines('./../temp/split_done.txt')


        rows = len(content)


        self.ui.tableWidget.setRowCount(rows)

        # 给每个单元格设置QTableWidgetItem
        for i in range(0,rows):
            for j in range(0,2):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(''))
        #在表格中显示文本
        for i in range(0,rows):
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(content[i]))


    #视频选择
    def select_video(self):
        self.video_path = QFileDialog.getOpenFileName(self.ui, 'Open file', './../test_video')[0]
        if self.video_path!='':
            self.after_select_video()

    def after_select_video(self,flag=0):
        # 此时会有一个多线程的问题
        # get_audio 应建立一个新线程在后台运行
        self.play_video()
        self.video_info=combine_video.get_video_info(self.video_path)


        self.audio_path = './../temp/audio_extract.wav'
        if flag==0:
            #分离音频
            #创建新线程
            thread_audio=threading.Thread(target=combine_video.get_audio,
                                          args=(self.video_path,))


            #开始新线程
            thread_audio.start()




    #播放视频
    def play_video(self):
        self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(self.video_path)))
        self.player.play()

    #生成.srt文件
    def make_srt(self):
        flag = 0
        choice = QMessageBox.question(
            self.ui,
            '确认',
            '请检查好文本内容与说话内容一致，时间点合法，否则会出错！！！',
            QMessageBox.Yes|QMessageBox.No,
            QMessageBox.No
            )


        if choice == QMessageBox.Yes:
            self.time_lst[0].clear()
            self.time_lst[1].clear()
            # 获取表格中的内容来填充time_point_lst
            for i in range(0, self.ui.tableWidget.rowCount()):
                self.time_lst[0].append(self.ui.tableWidget.item(i, 0).text())
                self.time_lst[1].append(self.ui.tableWidget.item(i, 1).text())

            #存储表格中最后的内容
            with open('./../temp/final_text_in_table.txt', 'w',encoding='utf-8')as f:
                for i in range(0, self.ui.tableWidget.rowCount()):
                    f.write(self.ui.tableWidget.item(i, 2).text())

            #是否要英文翻译
            if self.ui.eng_radio.isChecked():
                save_path = QFileDialog.getSaveFileName(self.ui, 'save file', './../output','.srt')[0]
                if save_path!='':
                    if self.have_translated_flag==0:
                        self.translate()
                    res = make_srt_eng(self.time_lst, './../temp/final_text_in_table.txt','./../temp/translate_done.txt',save_path)
                    flag = 1
                    self.have_translated_flag=1
                    self.srt_path = save_path
            else:
                save_path = QFileDialog.getSaveFileName(self.ui, 'save file', './../output', '.srt')[0]
                if save_path!='':
                    res = make_srt(self.time_lst, './../temp/final_text_in_table.txt',save_path)
                    self.srt_path=save_path
                    flag = 1
            if flag==1:
                #判断结果给出提示信息
                if res == 1:
                    QMessageBox.information(
                        self.ui,
                        '提示',
                        '字幕生成成功',
                    )
                if res == 0:
                    QMessageBox.critical(
                        self.ui,
                        '错误',
                        '字幕生成失败',
                    )


    def translate(self):

        #获得分行后的文本
        lines=read_lines('./../temp/final_text_in_table.txt')

        #写入翻译后的文本
        with open('./../temp/translate_done.txt','w',encoding='utf-8')as f:
            for each in lines:
                if translate.get_res(each) is not None:
                    f.write(translate.get_res(each)+'\n')
                else:
                    QMessageBox.critical(
                        self.ui,
                        '错误',
                        '翻译函数失败',
                    )


    def make_ass(self):
        flag=0
        choice = QMessageBox.question(
            self.ui,
            '确认',
            '请检查好文本内容与说话内容一致，时间点合法，否则会出错！！！你要继续吗?',
            QMessageBox.Yes|QMessageBox.No,
            QMessageBox.No
            )

        self.time_lst[0].clear()
        self.time_lst[1].clear()
        if choice==QMessageBox.Yes:
            # 获取表格中的内容来填充time_point_lst
            for i in range(0, self.ui.tableWidget.rowCount()):
                self.time_lst[0].append(self.ui.tableWidget.item(i, 0).text())
                self.time_lst[1].append(self.ui.tableWidget.item(i, 1).text())

            with open('./../temp/final_text_in_table.txt', 'w',encoding='utf-8')as f:
                for i in range(0, self.ui.tableWidget.rowCount()):
                    f.write(self.ui.tableWidget.item(i, 2).text())
            if self.ui.eng_radio.isChecked():
                save_path = QFileDialog.getSaveFileName(self.ui, 'save file', './../output', '.ass')[0]
                if save_path!='':
                    flag=1
                    if self.have_translated_flag==0:
                        self.translate()
                    res=make_ass.make_ass_eng(self.time_lst, './../temp/final_text_in_table.txt','./../temp/translate_done.txt',self.stylesheet,save_path)
                    self.have_translated_flag=1
            else:
                save_path = QFileDialog.getSaveFileName(self.ui, 'save file', './../output', '.ass')[0]
                if save_path!='':
                    flag=1
                    res=make_ass.make_ass(self.time_lst, './../temp/final_text_in_table.txt',self.stylesheet,save_path)

            if flag==1:
                #判断结果 给出提示
                if res == 1:
                    QMessageBox.information(
                        self.ui,
                        '提示',
                        '字幕生成成功',
                    )
                if res == 0:
                    QMessageBox.critical(
                        self.ui,
                        '错误',
                        '字幕生成失败',
                    )



    def auto_detect_time_point(self):
        QMessageBox.information(
            self.ui,
            '提示',
            '请稍等！',
        )
        #运行函数
        audio = handle_audio.audio_analysis(audio_path=self.audio_path, text_path=self.text_path)

        self.time_lst[0],self.time_lst[1]=audio.run()

        #转换成对应的时间格式
        modify_to_s_in_auto(self.time_lst)

        #将数据写到表格中
        for i in range(0,self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.item(i,0).setText(str(self.time_lst[0][i]))
            self.ui.tableWidget.item(i, 1).setText(str(self.time_lst[1][i]))

        #提示信息
        QMessageBox.information(
            self.ui,
            '提示',
            '部分时间点机器无法匹配，请自行录入时间点！',
        )
    def make_hard_zimu(self):
        # video_info :width, height, frame_nums, framerate
        make_hard_zimu.RealizeAddSubtitles(self.video_path, self.srt_path)
        QMessageBox.information(
            self.ui,
            '提示',
            '完成',
        )



if __name__ =="__main__":
    app = QApplication([])
    main_window = Stats()
    main_window.ui.show()
    app.exec_()
