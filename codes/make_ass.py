import other_func
Fontname=''
Fontsize=''
PrimaryColour=''
Bold=''
Italic=''
Underline=''
StrikeOut=''
infos='''[Script Info]
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
Style: Default,Arial,18,&H00FFFFFF,&H00E92616,&H00FFFFFF,&H00000000,,,0,0,100,100,0,0,1,2,3,2,20,20,20,134

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
# PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic,  不是所有样式在迅雷中都能显示


def make_ass(num_data,text_path):
    for i in range(0,len(num_data[0])):
        num_data[0][i]=num_data[0][i].replace(',','.')
        num_data[1][i]=num_data[1][i].replace(',', '.')
    with open(text_path, 'r')as f:
        text=f.readlines()
    try:
        with open('./../done/done.ass','w',encoding='utf-8')as f:
            f.write(infos)
            for i in range(0,len(text)):
                temp=''
                temp+=f'Dialogue: 0,{str(num_data[0][i])},{num_data[1][i]},*Default,,0000,0000,0000,,{text[i][0:len(text[i])-1]}'+r'\N'
                print(temp)
                f.write(temp+'\n')
        return 1
    except:
        return 0
'''
{\fn微软雅黑\fs14}You're too hard on him.'''

def make_ass_eng(num_data,text_path,text_eng_path):
    for i in range(0,len(num_data[0])):
        num_data[0][i]=num_data[0][i].replace(',','.')
        num_data[1][i]=num_data[1][i].replace(',', '.')
    with open(text_path, 'r')as f:
        text=f.readlines()
    with open(text_eng_path,'r')as f:
        text_eng=f.readlines()
    try:
        with open('./../done/done_eng.ass','w',encoding='utf-8')as f:
            f.write(infos)
            for i in range(0,len(text)):
                temp=''
                temp+=f'Dialogue: 0,{str(num_data[0][i])},{num_data[1][i]},*Default,,0000,0000,0000,,{text[i][0:len(text[i])-1]}'+r'\N'+f'{{\\fn微软雅黑\\fs14}}{text_eng[i]}'
                print(temp)
                f.write(temp)
        return 1
    except:
        return 0
