
#  将函数中取得的ms数  转化成具体时间格式
def modify_to_s(time_in_ms):
    hour=int(time_in_ms/3600000)
    minute=int(time_in_ms/60000)%60
    second=int(time_in_ms/1000)%60
    ms= int(time_in_ms % 1000)
    res=f'{hour}:{minute}:{second},{ms}'
    return res

'''
<b>字幕</b>
{\\fn字体名称}
{\\fs字号大小}
<i>字幕</i>
<font color=#ED935E>
 {\pos(x,y)}
'''
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
    with open(text_path,'r',encoding='utf-8')as f:
        file=f.readlines()
    length=len(file)
    #字符串格式化生成文件
    path='a.srt'
    with open(path,'w',encoding='utf-8')as f2:
        for i in range(length):
            f2.write(str(i+1))
            f2.write('\n')
            f2.write(str(modify_to_s(num_data[i][0]))+' --> '+str(modify_to_s(num_data[i][1]))+'\n')
            f2.write(file[i])
            f2.write('\n')

