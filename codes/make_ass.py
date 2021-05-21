
infos1='''[Script Info]
;
Title:
Original Script:
Original Translation:
Original Timing:
Original Editing:
Script Updated By:
Update Details:
ScriptType: v4.00+
Collisions: Normal
PlayResX: 384
PlayResY: 288
Timer: 100.0000
Synch Point:
WrapStyle: 0
ScaledBorderAndShadow: no

[V4+ Styles]
Format: Name, Fontname, 50, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
'''
infos2='''
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''



'''
主函数样式表
self.style_dic['font']=['Arial']
self.style_dic['font-size'] =[72]
self.style_dic['text-decoration'] = []
self.style_dic['color'] = [255,255,255]
'''

#将主函数的样式标 变成字幕样式中需要的格式
def convert_style_dic(style_dic):
    Fontname = 'Arial'
    Fontsize = '73'
    Color = '&H000634FF'
    Bold = '0'
    Italic = '0'
    Underline = '0'
    StrikeOut = '0'
    Fontname=style_dic['font'][-1][1:-1]
    Fontsize=style_dic['font-size']
    # 5cff38
    if style_dic['color'][3] is not None:
        Color='&H00'+str(style_dic['color'][4])[-6:].upper()
    if 'bold' in style_dic['font']:
        Bold=1
    if 'italic' in style_dic['font']:
        Italic=1
    if style_dic['text-decoration'] == "line-through underline":
        Underline=1
        StrikeOut=1
    if style_dic['text-decoration'] == "line-through":
        Underline =0
        StrikeOut = 1
    if style_dic['text-decoration'] == "underline":
        Underline = 1
        StrikeOut = 0
    return Fontname,Fontsize,Color,Bold,Italic,Underline,StrikeOut






def make_ass(num_data,text_path,style_dic,save_path):
    Fontname, Fontsize, Color, Bold, Italic, Underline, StrikeOut=convert_style_dic(style_dic)
    for i in range(0,len(num_data[0])):
        num_data[0][i]=num_data[0][i].replace(',','.')
        num_data[1][i]=num_data[1][i].replace(',', '.')
    with open(text_path, 'r')as f:
        text=f.readlines()
    try:
        with open(save_path,'w',encoding='utf-8')as f:
            f.write(infos1)
            f.write(f'Style: Default,{Fontname},{Fontsize},{Color},&H00E92616,&H00FFFFFF,&H00000000,{Bold},{Italic},{Underline},{StrikeOut},100,100,0,0,1,2,3,2,20,20,20,134'+'\n')
            f.write(infos2)
            for i in range(0,len(text)):
                temp=''
                temp+=f'Dialogue: 0,{str(num_data[0][i])},{num_data[1][i]},*Default,,0000,0000,0000,,{text[i][0:len(text[i])-1]}'+r'\N'
                print(temp)
                f.write(temp+'\n')
        return 1
    except:
        return 0


def make_ass_eng(num_data,text_path,text_eng_path,style_dic,save_path):
    Fontname, Fontsize, Color, Bold, Italic, Underline, StrikeOut=convert_style_dic(style_dic)
    for i in range(0,len(num_data[0])):
        num_data[0][i]=num_data[0][i].replace(',','.')
        num_data[1][i]=num_data[1][i].replace(',', '.')
    with open(text_path, 'r')as f:
        text=f.readlines()
    with open(text_eng_path,'r')as f:
        text_eng=f.readlines()
    try:
        with open(save_path,'w',encoding='utf-8')as f:
            f.write(infos1)
            f.write(
                f'Style: Default,{Fontname},{Fontsize},{Color},&H00E92616,&H00FFFFFF,&H00000000,{Bold},{Italic},{Underline},{StrikeOut},100,100,0,0,1,2,3,2,20,20,20,134' + '\n')
            f.write(infos2)
            for i in range(0,len(text)):
                temp=''
                temp+=f'Dialogue: 0,{str(num_data[0][i])},{num_data[1][i]},*Default,,0000,0000,0000,,{text[i][0:len(text[i])-1]}'+r'\N'+f'{{\\fn微软雅黑\\fs14}}{text_eng[i]}'
                print(temp)
                f.write(temp)
        return 1
    except:
        return 0

