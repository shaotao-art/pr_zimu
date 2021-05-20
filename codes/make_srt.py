
#  将函数中取得的ms数  转化成具体时间格式
def modify_to_s(time_in_ms):
    hour=int(time_in_ms/3600000)
    minute=int(time_in_ms/60000)%60
    second=int(time_in_ms/1000)%60
    ms= int(time_in_ms % 1000)
    res=f'{hour}:{minute}:{second},{ms}'
    return res

def modify_to_s_in_auto(time_lst):
    for i in range(0,len(time_lst[0])):
        if time_lst[0][i]!=' ':
            time_lst[0][i]=modify_to_s(int(time_lst[0][i]*1000))
    for i in range(0,len(time_lst[1])):
        if time_lst[1][i]!=' ':
            time_lst[1][i]=modify_to_s(int(time_lst[1][i]*1000))
    return time_lst

'''
.srt文件格式
3
00:00:29,154 --> 00:00:32,364
I don't understand why we can't continue construction.
我不明白为什么不能继续施工

4
00:00:32,449 --> 00:00:34,366
We could become partners.
我们本可以成为搭档的

5

首先是标号（从 1 开始）
时间格式  记得箭头的左右有一个空格  时间的各位的长度可以是不固定的
文本
'''

#通过表格中文字生成srt文件
def make_srt(num_data,text_path):
    #读取文本文件获取长度
    with open(text_path,'r')as f:
        file=f.readlines()
    if len(num_data[0])==len(file):
        length=len(file)
        #字符串格式化生成文件

        with open('./../done/done.srt','w',encoding='utf-8')as f2:
            for i in range(length):
                f2.write(str(i+1))
                f2.write('\n')
                f2.write(str(num_data[0][i])+' --> '+str(num_data[1][i])+'\n')
                f2.write(file[i])
                f2.write('\n')
        return 1
    else:
        print('length of num_data and text does not match')
        print(len(num_data[0]),len(file))
        return 0

#通过表格中文字生成srt文件
def make_srt_eng(num_data,text_path,eng_text_path):
    #读取文本文件获取长度
    with open(text_path,'r')as f:
        file=f.readlines()
    with open(eng_text_path,'r')as f:
        eng_file=f.readlines()
    if len(num_data[0])==len(file):
        length=len(file)
        #字符串格式化生成文件
        with open('./../done/done_eng.srt','w',encoding='utf-8')as f2:
            for i in range(length):
                f2.write(str(i+1))
                f2.write('\n')
                f2.write(str(num_data[0][i])+' --> '+str(num_data[1][i])+'\n')
                f2.write(file[i])
                f2.write(eng_file[i])
                f2.write('\n')
        return 1
    else:
        print('length of num_data and text does not match')
        print(len(num_data[0]),len(file))
        return 0

