from PIL import Image, ImageDraw, ImageFont

'''
用户的使用流程：
    1，用户输入文件地址（正确与否）
        没有问题直接生成字幕图片
    2，用户输入地址后部分行产生问题
        自行对done文件进行修改（成功与否）
        正确后生成图片
'''
'''
用户会遇到的问题：
    1，字幕超过图片的大小
       在done. txt文档中对用户进行提示  使其更改
    2，更丰富的选择：
        如字体的选择与大小的选择
'''
'''
步骤1将整个文章分解成
    一句话一行的形式
具体实现：
    1.对输入的文章进行读入
    2.读到标点就产生回车
'''


def spilt():
    path = input('请输入文本文件的路径:')
    chinese_char = ['！', '？', '。', '，', '‘', '\b', ',']
    try:
        with open(path, 'r', encoding='utf-8')as f:
            lines = list(f.readlines())
        with open('done.txt', 'w', encoding='utf-8')as f1:
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
        check('done.txt')
    except (SyntaxError, FileNotFoundError, OSError):
        print('路径错误！ 请重新输入正确的路径，readme.txt中有教学呦')
        spilt()
    print('-----完成，现在请查看该目录下done.txt文件')
    print('-----查看是否每一行为您想要展示的字幕')
    print('-----并查看其中的提示信息，进行适当的修改后再次打开此程序。')


def check(path):
    with open(path, 'r+', encoding='utf-8')as f:
        f.write('\n' * 2)
        lines = list(f.readlines())
        for each_line in lines:
            #img = Image.new(mode='RGB', size=(1920, 1080), color=(0, 0, 0))   # 此为生成黑色背景的图片
            img = Image.new(mode='RGBA', size=(1920, 1080))                    # 此为生成透明背景的图片
            draw = ImageDraw.Draw(img)
            ttf_font = ImageFont.truetype('simhei.ttf', 45)  # 字体大小
            (zimu_x, zimu_y) = draw.textsize(text=each_line, font=ttf_font)
            if zimu_x > 980:
                f.write(each_line + '-------此句太长了，字幕不好加，请把它修改一下' + '\n')
        f.write('\n' * 2 + '#########修改好这个文件后不要忘记把我们这些没用的语句删掉呦')


'''
因为要使字幕居中，我们设置
 1，空白字幕图片的大小为1920*1080
 2. 文字离字幕图片底边的大小恒定
 3. 获得文字的大小 计算xy坐标使其居中 
'''


def write_text():
    with open('done.txt', encoding='utf-8')as f:
        lines = list(f.readlines())
        for each_line in lines:
            img = Image.new(mode='RGBA', size=(1920, 1080))
            draw = ImageDraw.Draw(img)
            ttf_font = ImageFont.truetype('simhei.ttf', 45)  # 字体大小
            (zimu_x, zimu_y) = draw.textsize(text=each_line, font=ttf_font)
            draw.text(xy=((1980 - zimu_x) / 2 - 10, 1080 - zimu_y - 90), text=each_line, fill=(255, 255, 255),
                      font=ttf_font)  # 文字位置，内容，字体
            img.save('{}.png'.format(lines.index(each_line)))
            print('--请等待正在生成第{}张图片'.format(lines.index(each_line)))

#/home/starfish/桌面/shuijiaonan.txt
def main():
    print("#####  欢迎使用我的pr字幕生成器   #####")
    print('     初次使用请输入数字：1')
    print('     已修改好done.txt文件请输入数字：2')
    num = int(input('请输入你的选项（1或者2）：'))
    if num == 1:
        spilt()
        input('按任意键退出........')
    elif num == 2:
        write_text()
        input('按任意键退出........')
    else:
        main()


main()
