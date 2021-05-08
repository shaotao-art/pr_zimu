
#将输入的文本分行
def split_sentence(path):
    chinese_char = ['！', '？', '。', '，', '‘', '\b', ',']
    try:
        with open(path, 'r', encoding='utf-8')as f:
            lines = list(f.readlines())
        with open('./../docs/done.txt', 'w', encoding='utf-8')as f1:
            for each_line in lines:
                for each_char in each_line:
                    if each_char == '\n':
                        pass
                    elif each_char == '　':  # 该字符为\u3000 是全角的空白符 用于缩进
                        pass  # \xa0 是不间断空白符 &nbsp; 不在ascii编码内
                    elif each_char in chinese_char:
                        f1.write('\n')
                    else:
                        f1.write(each_char)
    except (SyntaxError, FileNotFoundError, OSError):
        print('路径错误！ 请重新输入正确的路径')
        split_sentence()
split_sentence('./../docs/test.txt')
# 将选择样式的字幕参数  变成stylesheet样式
font = {'font-family': 'Arial',
        'font-style': '',
        'font-weight': '',
        'font-size': 9,
        'text-decoration': '',
        'color': [111, 222, 255]}
style_sheet=''
for k,v in font.items():
    if v !='':
        if k=='font-size':
            style_sheet += (str(k) + ':' + str(v) + 'px;')
        elif k=='color':
            style_sheet += (str(k) + ':' + f'rgb({v[0]},{v[1]},{v[2]})')
        else:
            style_sheet+=(str(k)+':'+str(v) +';')




