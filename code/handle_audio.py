'''
根据输入的音频来划分语句之间的停顿，并找出正确的时间点

1，是否需要所有的数据  减少数据输入量
2，如何界定一个最短的语句长度（即如果语音中只说了1-2个字，我们如何来识别他，而不是将其变为0）
3，开头和结尾的一段静默时间，是否需要我们来处理
'''

'''
思路：
1，先将分贝数小于某个值的部分全部变为0
2，找出这一段空白的左右边界
3，选定中间值作为分割点
'''

import wave
import matplotlib.pyplot as plt
import numpy as np
# 文件路径
path1='C:\\Users\starfish\Documents\WPS Cloud Files\\262233160\录音-001.wav'
path2='C:\\Users\starfish\Documents\Tencent Files\\2842226412\FileRecv\MobileFile\\1.wav'
path3='C:\\Users\starfish\Documents\Adobe\Premiere Pro\\14.0\99_1.aac'

max_fengbei=2500
max_count=30000


def get_data(path):
    # 打开文件
    f = wave.open(f=path, mode='rb')
    # 获取音频文件信息
    nchannels, sampwidth, framerate, nframes = f.getparams()[:4]  # nchannels=1,声道数 sampwidth=2, framerate=48000,采样率 nframes=448320采样数
    # 读取音频的每一帧
    data = f.readframes(nframes)
    # 使用np生成数据矩阵
    _data = np.fromstring(data, dtype=np.int16)

    return _data,framerate,nframes

def biaozhu(_data,nframes):
    '''
    1，如果连续初恋30000个0
    则认为该段是间隔
    2，算出头部尾部
    3，计算平均值
    :param _data:
    :return:

    tips:放大生成的图像可得  实际上看似连续的波形放大之后中间的空白还是很多的
    所以不能检测 第一个 和 最后一个小于3000的值来计算
    而是连续出现多少个小于三千的数

    下面的代码是错误的
        for j in range(len(_data)):
        if abs(_data[j]) <3000:
            if count == 0:
                print(j)
                count = 1
        else:
            if count == 1:
                print(j)
                count = 0
    '''
    start_lst = []
    end_lst = []
    global max_count
    global max_fengbei
    for i in range(0,len(_data)):
        if abs(_data[i])<max_fengbei:
            _data[i]=0
    # for i in range(len(_data)-1):
    #     #此处有待修正   如果有空隙很大  会出现多个值
    #     if count>= max_count:
    #         if abs(_data[i])==0 and abs(_data[i + 1]) ==0:
    #             count += 1
    #         else:
    #             count = 0
    #             end_lst.append(i)
        # if abs(_data[i])==0  and abs(_data[i + 1])==0 :
        #     count+=1
        # 并不能检测连续的30000个   中间的小空白也会被算进去
    i=0
    while i < len(_data) - max_count:
        temp=_data[i:i+max_count]
        if np.sum(temp)==0:
            if i-max_count not in end_lst or i-2*max_count not in end_lst:
                end_lst.append(i)
            i=i+max_count
        else:
            i+=10

    print(start_lst,end_lst)
    print(len(end_lst))
    for each in end_lst:
        print(each/48000)

def handle_data(_data,nframes):
    times = np.arange(0, nframes)
    for i in range(0,len(_data)):
        if abs(_data[i])<max_fengbei:
            _data[i]=0
    # 绘图并显示
    plt.plot(times, _data)
    plt.show()

def run(path):
    _data, nframes=get_data(path)
    # biaozhu(_data,nframes)
    handle_data(_data,nframes)


run(path1)