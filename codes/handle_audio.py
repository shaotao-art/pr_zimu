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

audio_path=['./../test_audio/录音-001.wav',
            './../test_audio/录音-002.wav',
            './../test_audio/录音-003.wav',
            './../test_audio/录音-004.wav',
            './../test_audio/录音-005.wav',
            './../test_audio/录音-006.wav',
            './../test_audio/录音-007.wav',
            './../test_audio/录音-008.wav']
text_path=['./../docs/1.txt',
           './../docs/2.txt',
           './../docs/3.txt',
           './../docs/4.txt',
           './../docs/5.txt',
           './../docs/6.txt',
           './../docs/7.txt',
           './../docs/8.txt']


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

        #寻找间隔的步长
        self.step_for_find_left_and_right=100

        # 分割空白区间的重要参数
        self.step_for_slice_move=50

        # 修正两端间隔的重叠
        self.parm_for_check_chongdie=0.1

        # 两段间隔之间的说话长度是否太短
        self.parm_for_check_jianfeng=0.1

        # 判断间隔的长度是否过短
        self.parm_for_check_blank_len=0.1

        #音频基本信息
        #0 nchannels=1,声道数 1 sampwidth=2, 2 framerate=48000,采样率 3 nframes=448320采样数
        self.audio_info=[None]*4
        self._data=None

        #音频间隔节点列表
        self.start_lst=[]
        self.end_lst=[]
        self.duration_lst=[]

        #平均每秒说话字数
        self.words_per_sec=0

        #文章字数
        self.actual_words_num=0
        self.cal_words_num=0




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
        '''
        获取音频信息
        :return:
        '''
        # 打开文件
        f = wave.open(f=self.path, mode='rb')
        # 获取音频文件信息
        self.audio_info[0], self.audio_info[1], self.audio_info[2], self.audio_info[3] = f.getparams()[:4]  # nchannels=1,声道数 sampwidth=2, framerate=48000,采样率 nframes=448320采样数
        # 读取音频的每一帧
        data = f.readframes(self.audio_info[3])
        # 使用np生成数据矩阵


        #处理单 双声道
        if self.audio_info[0]==2:
            self._data=np.fromstring(data,dtype=np.int16)[0:self.audio_info[3]*2:2]
            self._data1 = np.fromstring(data, dtype=np.int16)[1: self.audio_info[3] * 2:2]
            self._data=(self._data+self._data1)/2
        elif self.audio_info[0]==1:
            self._data = np.fromstring(data, dtype=np.int16)
        else:
            print('mind the nchannels')








    def _find_left_and_right(self, num_in, data):
        '''
        make_start_end_lst的内部函数
        :param num_in: 切片得到的间隔点
        :param data: 音频数据
        :return: 间隔的最大左右端点
        '''
        l=num_in
        while data[l]==0 and l>=self.step_for_find_left_and_right:
            l-=self.step_for_find_left_and_right
        r=num_in
        while data[r]==0 and r<self.audio_info[3]-self.step_for_find_left_and_right:
            r+=self.step_for_find_left_and_right
        return l + self.step_for_find_left_and_right, r - self.step_for_find_left_and_right


    def make_start_end_lst(self, _data):
        '''
        #分割生成start—end—lst
        :param _data:
        :return:
        '''
        #将杂音变0
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
        '''
        做出标注出间隔点后的图像
        :param _data:
        :return:
        '''
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

        #生成duration——lst
        for i in range(len(self.start_lst)):
            self.duration_lst.append(self.end_lst[i]-self.start_lst[i])
    def dui_ying_wenben(self):

        temp_res=match.get_res(actual_lst=self.actual_each_sentence_len,cal_lst=self.cal_each_sentence_len,duration_lst=self.duration_lst)
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

        self.make_start_end_lst(self._data)
        #打印start_end_lst

        self.count_words()

        #计算每段语音说的字的长度
        self.caulate_words()
        print('self.cal_each_sentence_len',self.cal_each_sentence_len)
        print('self.actual_each_sentence_len',self.actual_each_sentence_len)
        # self.plot_zero_audio(self._data)
        # res=self.dui_ying_wenben()
        # return res
for i in range(4,8):
    test=audio_analysis(audio_path[i],text_path[i])
    test.run()

'''
001


[14, 22, 2, 18, 13, 6, 4, 16, 13, 11, 9, 9, 8, 16, 17, 4, 4, 4, 3, 9, 11, 6, 19]
[3.3536284004753028, 5.5247273836188295,6.544580796449941, 
3.747804872919225, 11.174590155315098, 8.008664836955953, 
1.8332334353344557, 
5.143064449982645, 12.538565885359162, 
7.896042987686267, 5.211888913425258, 
5.987728319505343, 
4.235832886421221, 
6.90747342187452, 8.515463158669549, 
14.859827334195604, 
11.34352292921965, 
8.953437016940564, 
8.94092347813283, 
6.882446344259034, 
9.42895149163486, 8.803274551247691, 
7.789677907820436, 8.515463158669549, 
4.429792737941286, 
4.442306276749018, 
4.70509059171161, 
2.834316539953967, 
7.501866515242337, 
9.347613489384514, 
4.536157817807095, 
2.7154379212803823, 11.82529417331777, 3.4850205579566014]
'''
'''
002


6, 10, 4, 7, 10, 8, 5, 5, 8, 10
6.545338441890168, 
8.6845466155811, 
3.5440613026819934, 
6.028097062579824, 
8.499361430395911, 
8.212005108556836, 
5.574712643678156, 
5.727969348659001, 
8.652618135376752, 
7.081736909323125, 4.4125159642400975
'''
'''
003

9, 6, 4, 8, 19, 2, 13, 8, 15, 9, 13, 3, 9, 13, 6, 8, 9, 14, 4, 7, 6, 13, 6, 7, 7, 9
10.003604902667632, 
5.524103690109461, 
4.350462082978306, 
7.564150881562565, 
6.1754440584649695, 7.496558956544534, 6.60557449039785,
2.1014943960149406, 
6.1754440584649695, 5.55482729239038, 
6.728468899521534, 
9.112620436520956, 4.6761322671560634, 
9.008160188765817, 
13.340188110375573, 
2.636085075702949,
8.627187520482398, 
12.0620862554893, 
4.78673723536738,
8.319951497673223, 
8.473569509077768, 
13.83176574687029, 
3.527069541849622, 
6.372075113062849, 
6.974257717768924,    
13.721160778658952, 
6.673166415415886, 
7.601019204299672,
7.250770138297165, 
6.64858753359113, 3.047781346267283
'''

'''
004
6, 9, 2, 11, 14, 10, 14, 10, 10, 10, 10, 12, 7, 9, 17, 12, 13, 4, 18, 12

6.629458769256121, 
4.8377131559436535, 4.794464123898183, 
1.6002141856825103, 
6.369964576983281, 4.553505231073401, 
13.431913666694138, 
9.29854188977675, 
12.054123074388345, 
5.177526979158078, 6.017793887470125, 
4.479364033281155, 5.783013427794701,
6.22168218139881, 2.5331575912348567, 
5.430842738281566, 4.294011038800555, 
11.460993492050408,
6.654172501853508, 
8.742482906334972,
10.81225801136835, 2.1500947359749407, 5.616195732762208,
10.36741082461485,
5.091028915067147, 9.378861520718333, 
3.867699151495163, 
4.819177856495595, 7.383227613477211, 5.813905593541503,
5.344344674190656, 3.323997034352059, 5.640909465359599
'''

'''
005
9, 5, 5, 4, 7, 8, 6, 16, 10, 9, 7, 7, 17, 4, 13, 16

9.53004628763412,
4.805453643219141, 
4.424251791713779, 
4.3664939354250905, 
6.249400050436434, 
7.664467529509382, 
5.082691353404861, 
6.624826116312933, 1.8771303293824846, 7.595158101962956, 
2.818583386888149, 7.508521317529919, 
8.253597663654052, 
6.930942754642996, 
6.520861974993284, 
13.84455815239938, 
7.190853107942108, 
3.7080543737340186, 10.101849064892198, 
2.9109959569500505, 5.325274349817371, 8.634799515159386


9.53004628763412,
4.805453643219141, 
4.424251791713779, 
4.3664939354250905, 
6.249400050436434, 
7.664467529509382, 
5.082691353404861, 
6.624826116312933, 1.8771303293824846, 7.595158101962956, 
2.818583386888149, 7.508521317529919, 
8.253597663654052, 
6.930942754642996, 
6.520861974993284, 
13.84455815239938, 7.190853107942108, 
3.7080543737340186, 
10.101849064892198, 
2.9109959569500505, 5.325274349817371, 8.634799515159386

****************************
'''

'''
006


[3, 8, 6, 7, 9, 15, 15, 7, 9, 5, 14, 11, 12],
[3.338151790860048, 
2.9494628837051122, 5.710297327173268, 
6.316194741267731, 
7.105004582258627, 
7.69946996967207,
11.294842360855235, 4.8528953260962036, 
5.098683899738287, 2.7379703901061068, 6.470527101461585, 
7.505125516094593, 
8.191047116956247,
4.407046285536114, 
8.288219343744972, 3.7096926579934433, 
6.293330687905682, 5.881777727388674, 
4.721427019264379, 2.995190990429227, 5.407348620126033],

'''

'''
007
******************
[2, 26, 9, 17, 7, 17, 10, 4, 9, 6, 6, 6, 12, 5, 8, 4, 13, 20]

[2.6237713103215965, 
11.088826593837606, 7.113586871518466, 6.231456862013788, 
7.74691098090644, 
8.73082522227703, 9.516825679463887, 
7.6620907876848365, 
10.031401518341617, 6.638593789477485, 
4.908261847756789, 5.5415859571447434, 
4.648146588543858, 
10.698653705018241, 
5.1627224274215795, 
5.852593332290629, 
6.304967696139155, 
6.423715966649407, 6.078780514214892, 
4.987427361430252, 
6.94960116462337, 3.511555999374385,
4.21839094288772, 
6.265384939302442, 7.515069119434046, 
7.181443026095773, 14.334612654450961],

'''

'''
008


[8, 7, 11, 18, 7, 7, 9]

[7.261067196978558, 
7.1770918631661615, 
4.529069670281922, 7.037132973478834, 
3.364611708083361, 15.585821955580807,
6.6788382158792725, 
6.606059593241861, 
8.733434716489244]


'''
