import wave
import matplotlib.pyplot as plt
import numpy as np
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

test_num=8

class audio_analysis():
    def __init__(self):
        # 文件路径
        self.path=audio_path[test_num]
        self.text=text_path[test_num]
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

        self.cal_each_sentence_len=[]

        self.actual_each_sentence_len=[]


    def get_data(self):
        # 打开文件
        f = wave.open(f=self.path, mode='rb')
        # 获取音频文件信息
        self.audio_info[0], self.audio_info[1], self.audio_info[2], self.audio_info[3] = f.getparams()[:4]  # nchannels=1,声道数 sampwidth=2, framerate=48000,采样率 nframes=448320采样数
        # 读取音频的每一帧
        data = f.readframes(self.audio_info[3])
        # 使用np生成数据矩阵
        self._data = np.fromstring(data, dtype=np.int16)


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




    def plot(self):
        times = np.arange(0, self.audio_info[3],dtype=np.float32)

        times=times/self.audio_info[2]

        plt.plot(times,self._data)
        plt.show()


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

    def dui_ying_wenben(self):
        #计算某一段说话时间的的时间间隔
        #计算该段应该说了多少个字
        #对应到文本
        #如果该对应的文本太过离谱就直接跳到下一个间隔
        #找出离对应文本最近的换行符'
        pass

    def count_words(self):
        with open(self.text, 'r', encoding='utf-8')as f:
            text = f.readlines()
        total_len = 0
        for each in text:
            if len(each)!=1:
                self.actual_each_sentence_len.append(len(each) - 1)
                total_len += len(each) - 1
        self.actual_words_num=total_len


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


test=audio_analysis()
test.get_data()


test._make_start_end_lst(test._data)
#打印start_end_lst

test.count_words()

#计算每段语音说的字的长度
test.caulate_words()
test.print_info()

test.plot_zero_audio(test._data)



'''
在大学作息时间实现的极度自由                        14
你以为每天能美美的从晚上8点睡到第二天11点             22
做梦                                             2
进入大学你就会发现这样一个可悲的事实                  18
实际上每天睡觉不足五个小时                          13
甚至彻夜happy                                    6
在宿舍里                                         4
每当我盖起被子准备美美的睡一觉时                     16
床底下传来不断的键盘敲击声                         13
室友连麦打游戏的叫喊声                             11
我就不得不塞上耳机                                9
沉浸在自己的世界里                                9
终于大家都上床了                                  8
我摘掉耳机想到终于能好好的睡觉时                    16
耳边又响起了室友那富有节奏的交响曲                   17
你高我低                                         4
你低我高                                         4
你应我和                                         4
就这样                                          3
我从第一个上床的人                                9
变成了最后一个睡着的人                            11
我彻底崩溃了                                     6
我就想怎么在大学好好的睡一个觉就那么难               18
'''


'''
每当想到这里                   6                6.440914644789665
我就痛恨的敲打着自己            10                  8.57866992494327
你说说你                      4               3.3253971024611646
为啥睡的那么早                 7                 5.909303543375805
你就没有其他事情了吗            10                  8.313492756152904
你就不能再学学习               8                  8.124978181183444
再打打游戏                    5                6.016128469191834
再听听音乐                    5                5.613964042590334
为啥就这么不争气               8                  8.42157444580206
早早上床睡觉来活遭罪            9                   6.885809041717572
                                          4.343375807296204
'''


'''
观看视频的小伙伴                     8                   7.0155910730903
如果是个女同学                      7                   6.900298760877019
也许对此并不能感同身受               11                     4.334775439570307
如果你也恰巧有个喜欢在深夜连麦的室友    18                         6.773153967968918
请说出你的故事                      7                   3.1947822963773187
并提出宝贵建议                      7                   14.954598142131815
让我能好好地睡个觉                    8                   3.9705810327657427
                                                 1.9707442900755878
                                                   4.975886895335735       
'''

'''
[0.0020833333333333333, 1.91875, 4.640625, 6.344791666666667, 7.734375, 10.259375, 10.371875, 12.644791666666666, 14.725, 16.894791666666666, 19.380208333333332, 21.188541666666666, 22.955208333333335, 24.2, 24.203125, 25.848958333333332, 28.534375, 29.775, 31.390625, 33.354166666666664, 35.125, 36.405208333333334, 38.378125, 39.99791666666667, 40.86145833333333, 42.603125, 44.946875, 46.541666666666664, 48.7, 51.73854166666667, 52.78541666666667, 53.70729166666667]
[1.4354166666666666, 2.597916666666667, 5.034375, 6.586458333333334, 8.832291666666666, 10.355208333333334, 11.036458333333334, 12.971875, 15.483333333333333, 17.532291666666666, 19.965625, 22.051041666666666, 23.182291666666668, 24.910416666666666, 24.992708333333333, 26.563541666666666, 28.823958333333334, 30.3125, 32.192708333333336, 33.94166666666667, 35.28541666666667, 37.459375, 38.717708333333334, 40.21458333333333, 41.82604166666667, 43.79270833333333, 45.157291666666666, 47.37708333333333, 49.09791666666667, 52.771875, 53.71458333333333, 54.67604166666667]

'''