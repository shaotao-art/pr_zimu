def split_sentence(path):
    '''
    #将输入的文本分行
    :param path: 带分行的文本路径
    :return:
    '''
    chars = ['！', '？', '。', '，', '‘', '’','\b', ',','“','”',',','：','；',':',';','\n']
    #不想文本中出现两个空行
    lst=[]
    with open(path, 'r', encoding='utf-8')as f:
        lines = list(f.readlines())
    with open('./../temp/split_done.txt', 'w', encoding='utf-8')as f:
        for each_line in lines:
            for each_char in each_line:
                if each_char in chars:
                    if len(lst)==0:
                        f.write('\n')
                        lst.append(each_char)
                    else:
                        pass
                else:
                    f.write(each_char)
                    lst.clear()
        f.write('\n')




def read_lines(text_path):
    '''
    读取文本文件
    :param text_path:
    :return:
    '''
    try:
        with open(text_path,'r',encoding='utf-8')as text:
            file=text.readlines()
    except:
        with open(text_path,'r',encoding='gbk')as text:
            file=text.readlines()
    return file



