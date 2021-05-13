import wave
import matplotlib.pyplot as plt
import numpy as np
import match
'''
类接口
a）测试要调的参数
        #判断是否为杂音的阈值
        self.max_fengbei=500
        #判断间隔的阈值
        self.max_count=2000 
        
        self.step_for_find_left_and_right=100

b）基本信息
        #0 nchannels=1,声道数 1 sampwidth=2, 2 framerate=48000,采样率 3 nframes=448320采样数
        self.audio_info=[None]*4


c）函数调用
    get_data(self)  读取音频数据到numpy
    plot(self)      绘制原始图像
    plot_zero_audio(self,_data)   绘制太小幅值变0后的图像
    caulate_words   计算出每小段语音的说的字的长度    
    count_words     计算文本中每句话长度
'''

audio_path=['C:\\Users\starfish\pr_zimu\\test_audio\录音-001.wav',
            'C:\\Users\starfish\pr_zimu\\test_audio\录音-002.wav',
            'C:\\Users\starfish\pr_zimu\\test_audio\录音-003.wav',
            'C:\\Users\starfish\pr_zimu\\test_audio\录音-004.wav',
            'C:\\Users\starfish\pr_zimu\\test_audio\录音-005.wav',
            'C:\\Users\starfish\pr_zimu\\test_audio\录音-006.wav',
            'C:\\Users\starfish\pr_zimu\\test_audio\录音-007.wav',
            'C:\\Users\starfish\pr_zimu\\test_audio\录音-008.wav',
            'C:\\Users\starfish\pr_zimu\\test_audio\maogai_3.wav']
text_path=['C:\\Users\starfish\pr_zimu\docs\\1.txt',
           'C:\\Users\starfish\pr_zimu\docs\\2.txt',
           'C:\\Users\starfish\pr_zimu\docs\\3.txt',
           'C:\\Users\starfish\pr_zimu\docs\\4.txt',
           'C:\\Users\starfish\pr_zimu\docs\\5.txt',
           'C:\\Users\starfish\pr_zimu\docs\\6.txt',
           'C:\\Users\starfish\pr_zimu\docs\\7.txt',
           'C:\\Users\starfish\pr_zimu\docs\\8.txt',
           'C:\\Users\starfish\pr_zimu\docs\\maogai_3.txt']


#[1, 2, 48000, 3114240]  [2, 2, 48000, 1881600]
class audio_analysis():
    def __init__(self,audio_path,text_path):
        # 文件路径
        self.path=audio_path
        self.text=text_path
        #判断是否为杂音的阈值
        self.max_fengbei=500
        #判断间隔的阈值
        self.max_count=2400
        #音频基本信息
        #0 nchannels=1,声道数 1 sampwidth=2, 2 framerate=48000,采样率 3 nframes=448320采样数
        self.audio_info=[None]*4
        self._data=None
        #音频间隔节点列表
        self.start_lst=[]
        self.end_lst=[]

        self.step_for_find_left_and_right=100
        self.words_per_sec=0
        self.actual_words_num=0
        self.cal_words_num=0
        self.step_for_slice_move=50  #分割空白区间的重要参数

        self.parm_for_check_chongdie=0.1     #修正两端间隔的重叠
        self.parm_for_check_jianfeng=0.1     #两段间隔之间的说话长度是否太短
        self.parm_for_check_blank_len=0.1   #判断间隔的长度是否过短

        # 根据语音计算出的每段的长度（可能有一句实际的话对应多个计算的话的情况）
        self.cal_each_sentence_len=[]
        #实际上每句话的长度
        self.actual_each_sentence_len=[]

        #计算出的一句实际的话对应计算出的话列表中元素的个数
        self.match_len_lst=[]

        #存储最终计算出的时间点的列表
        self.start_time_point_lst=[]
        self.end_time_point_lst = []



    def get_data(self):
        # 打开文件
        f = wave.open(f=self.path, mode='rb')
        # 获取音频文件信息
        self.audio_info[0], self.audio_info[1], self.audio_info[2], self.audio_info[3] = f.getparams()[:4]  # nchannels=1,声道数 sampwidth=2, framerate=48000,采样率 nframes=448320采样数
        # 读取音频的每一帧
        data = f.readframes(self.audio_info[3])
        # 使用np生成数据矩阵



        if self.audio_info[0]==2:
            self._data=np.fromstring(data,dtype=np.int16)[0:self.audio_info[3]*2:2]
            self._data1 = np.fromstring(data, dtype=np.int16)[1: self.audio_info[3] * 2:2]
            self._data=(self._data+self._data1)/2
        elif self.audio_info[0]==1:
            self._data = np.fromstring(data, dtype=np.int16)
        else:
            print('mind the nchannels')







    #make_start_end_lst的内部函数
    def _find_left_and_right(self, num_in, data):
        l=num_in
        while data[l]==0 and l>=self.step_for_find_left_and_right:
            l-=self.step_for_find_left_and_right
        r=num_in
        while data[r]==0 and r<self.audio_info[3]-self.step_for_find_left_and_right:
            r+=self.step_for_find_left_and_right
        return l + self.step_for_find_left_and_right, r - self.step_for_find_left_and_right

    #分割生成start—end—lst
    def _make_start_end_lst(self, _data):
        for i in range(0,len(_data)):
            if abs(_data[i])<self.max_fengbei:
                _data[i]=0

        i=0
        while i < len(_data) - self.max_count:
            #切片 音频 max_count
            temp=_data[i:i+self.max_count]
            #如果是空白
            if np.sum(temp)==0:
                l,r=self._find_left_and_right(i, _data)
                self.start_lst.append(l)
                self.end_lst.append(r)
                i=r+self.step_for_slice_move
            else:
                i+=self.step_for_slice_move
        for i in range(len(self.start_lst)):
            self.start_lst[i]/=self.audio_info[2]
            self.end_lst[i] /= self.audio_info[2]

        #检查列表的合法性
        self.check_start_end_lst()







    def plot_zero_audio(self,_data):
        # 将杂音幅度变为0
        for i in range(0, len(_data)):
            if abs(_data[i]) < self.max_fengbei:
                _data[i] = 0
        #将间隔点设置为30000标出
        for each in self.start_lst:
            self._data[int(each*self.audio_info[2])]=30000
        for each in self.end_lst:
            self._data[int(each*self.audio_info[2])]=30000
        times = np.arange(0, self.audio_info[3], dtype=np.float32)
        times = times / self.audio_info[2]
        plt.plot(times, self._data)
        plt.show()

    #将帧单位转换为秒
    def print_info(self):
        print('*******************************************************************')
        print(f'lst_len:  {len(self.start_lst)}  ')
        print(self.start_lst)
        print(self.end_lst)
        for i in range(0,len(self.start_lst)):
            print(f'start {self.start_lst[i]}  '.ljust(40),end='')
            print(f' end  {self.end_lst[i]}    '.ljust(40),end='')
            print(f' duration {self.end_lst[i]-self.start_lst[i]}'.ljust(40))

        print('********************************************************************')
        with open(self.text, 'r', encoding='utf-8')as f:
            text = f.readlines()

        print('actual each sentence words num')
        print(f'text_len {len(text)}')
        print(f'actual tatal word nums  {self.actual_words_num}')
        for i in range(0,len(self.actual_each_sentence_len)):

            #ljust 对中文的bug  一个中文字符 和 两个英文不是完全等宽的
            print(f'{text[i][0:len(text[i]) - 1]}'.ljust(61-len(text[i])), end='')

            print(self.actual_each_sentence_len[i])
        print('********************************************************************')
        print('cal each sentence words num')
        print(f'cal tatal word nums  {self.cal_words_num}')
        for each in self.cal_each_sentence_len:
            print(each)

    def caulate_words(self):
        #计算平均每秒说几个字
        temp=0
        for i in range(len(self.start_lst)):
            temp+=self.end_lst[i]-self.start_lst[i]  #计算秒数
        time_len=self.audio_info[3]/self.audio_info[2]-temp    # 总时长减去空白时间
        self.words_per_sec= self.actual_words_num / time_len

        #计算每段语音说的字的长度
        for i in range(1,len(self.end_lst)):
            temp=(self.start_lst[i] - self.end_lst[i - 1]) * self.words_per_sec
            self.cal_each_sentence_len.append(temp)
            self.cal_words_num+=temp



    def count_words(self):
        with open(self.text, 'r', encoding='utf-8')as f:
            text = f.readlines()
        total_len = 0
        #最后一行没有换行符
        for each in text:
            if len(each)!=1:
                self.actual_each_sentence_len.append(len(each) - 1)
                total_len += len(each) - 1
        self.actual_each_sentence_len[len(text)-1]+=1
        self.actual_words_num=total_len+1


    def check_start_end_lst(self):
        del_lst=[]
        #解决间隔重叠的情况  （重叠取大区间）
        for i in range(1,len(self.start_lst)):
            if self.start_lst[i]-self.start_lst[i-1]<self.parm_for_check_chongdie:
                del_lst.append(i)


        for each in del_lst:
            index = del_lst.index(each)
            if self.end_lst[each-index]-self.start_lst[each-index]>self.end_lst[each-index-1]-self.start_lst[each-index-1]:
                del self.start_lst[each-index-1]
                del self.end_lst[each-index-1]
            else:
                del self.start_lst[each - index]
                del self.end_lst[each - index]


        del_lst.clear()

        #解决小尖峰情况
        for i in range(1,len(self.start_lst)):
            if self.start_lst[i]-self.end_lst[i-1]<self.parm_for_check_jianfeng:
                del_lst.append(i)

        for each in del_lst:
            index=del_lst.index(each)
            del self.start_lst[each-index]
            del self.end_lst[each -index- 1]
        del_lst.clear()

        #解决每对start end的可能出现的问题  (间隔长度)
        for i in range(0,len(self.start_lst)):
            if self.end_lst[i]-self.start_lst[i]<self.parm_for_check_blank_len:
                del_lst.append(i)

        for each in del_lst:
            index=del_lst.index(each)
            del self.start_lst[each-index]
            del self.end_lst[each -index]
    def dui_ying_wenben(self):

        temp_res=match.get_res(actual_lst=self.actual_each_sentence_len,cal_lst=self.cal_each_sentence_len)
        self.match_len_lst =temp_res[2]
        res=match.make_time_point(self.actual_each_sentence_len,temp_res[1],self.start_lst,self.end_lst,self.match_len_lst)
        for i in range(0,len(res[0])):
            print(res[0][i],res[1][i])

        return res

        #计算某一段说话时间的的时间间隔
        #计算该段应该说了多少个字
        #对应到文本
        #如果该对应的文本太过离谱就直接跳到下一个间隔
        #找出离对应文本最近的换行符'
        pass
    def run(self):

        self.get_data()

        print(self.audio_info)

        self._make_start_end_lst(self._data)
        #打印start_end_lst

        self.count_words()

        #计算每段语音说的字的长度
        self.caulate_words()
        print('self.cal_each_sentence_len',self.cal_each_sentence_len)
        print('self.actual_each_sentence_len',self.actual_each_sentence_len)
        # self.plot_zero_audio(self._data)
        res=self.dui_ying_wenben()
        return res

test=audio_analysis(audio_path[0],text_path[0])
test.run()


