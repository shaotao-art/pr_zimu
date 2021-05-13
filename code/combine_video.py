from moviepy.editor import *
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
'''
震惊
opencv2竟然不支持中文文字写入图片
'''
#
# time_points = [[8978, 13879],
#                [13879, 18987],
#                [18987, 20099],
#                [20099, 24556],
#                [24556, 27860],
#                [27860, 29761],
#                [29761, 31423],
#                [31423, 35228],
#                [35228, 38395],
#                [38395, 41105],
#                [41105, 43045],
#                [43045, 45255],
#                [45255, 47570],
#                [47570, 51692],
#                [51692, 55933],
#                [55933, 57314],
#                [57314, 58429],
#                [58429, 59497],
#                [59497, 60583],
#                [60583, 62593],
#                [62593, 64697],
#                [64697, 66329],
#                [66329, 71039],
#                [71039, 72867],
#                [72867, 75112],
#                [75112, 76281],
#                [76281, 77981],
#                [77981, 79806],
#                [79806, 81625],
#                [81625, 83064],
#                [83064, 84761],
#                [84761, 87047],
#                [87047, 90227]]
#
#
# num_data=np.asarray(time_points,dtype=np.int32)
# num_data=num_data/1000*25


def get_video_info(path):
    #获取视频信息
    cap=cv2.VideoCapture(path)
    width=int(cap.get(3))
    height=int(cap.get(4))
    framerate=int(cap.get(5))
    frame_nums=int(cap.get(7))

    #截取视频中的一帧作为字幕样式时的显示图片
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_nums/2))
    success, img=cap.read()
    cv2.imwrite('./../media/one_frame.png', img)
    return width, height, frame_nums, framerate



#播放视频时（获得视频路径时）预先将视频和音频分离  取得音频文件
def get_audio(input_video_path,output_audio_path='./../media/file_audio.mp3'):
    video = VideoFileClip(input_video_path)
    audio = video.audio
    audio.write_audiofile(output_audio_path)

def read_lines(text_path):
    with open(text_path,'r',encoding='utf-8')as text:
        file=text.readlines()
    return file

'''
因为要使字幕居中，我们设置
 1，空白字幕图片的大小为1920*1080
 2. 文字离字幕图片底边的大小恒定
 3. 获得文字的大小 计算xy坐标使其居中
'''
def write_text(img,each_line):
    #将cv2图片转成pillow格式
    img_pillow=Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #创建对象
    draw = ImageDraw.Draw(img_pillow)
    # 字体大小
    ttf_font = ImageFont.truetype('simhei.ttf', 45)
    #获得字幕文本的大小
    (zimu_x, zimu_y) = draw.textsize(text=each_line, font=ttf_font)
    to_bottem=90
    width=1920
    height=1080
    color=[255,255,255]
    draw.text(xy=(int((width - zimu_x) / 2) ,int(height - zimu_y - to_bottem) ),
              text=each_line,
              fill=(color[0],color[1],color[2]),
              font=ttf_font)  # 文字位置，内容，字体
    img_done = cv2.cvtColor(np.asarray(img_pillow), cv2.COLOR_RGB2BGR)
    return img_done


#将视频的每一帧进行添加文字的处理，并保存图片
'''
读取视频的每一帧 并 计数：
    计数信息在范围内：
        1 写入文本
        2 写入帧
    否则
        直接写入帧

'''
def put_text_on_each_frame(framerate,frame_num,width,height,num_data,text,to_bottem,input_video_path):
    '''
    :param framerate: video fps
    :param width: framewidth
    :param height: frameheight
    :param num_data: 输入的带有时间序列的numpy数组   存储的是time in ms
    :param text: 读入的文本
    :param path: 读入的视频路径
    :return: None
    '''
    num_data_handle = num_data / 1000 * framerate
    cap=cv2.VideoCapture(input_video_path)
    # 创建视频写入对象
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # 视频参数
    out = cv2.VideoWriter('./../media/video_done.avi', fourcc, framerate, (width, height), True)

    global_flag=0
    q_flag=0

    while global_flag<frame_num:
        if global_flag==int(num_data_handle[q_flag][0]):

            # 持续的帧数
            lasting = int(num_data_handle[q_flag][1]) - int(num_data_handle[q_flag][0])
            flag = 0
            # 遍历其中的每一帧
            while flag < lasting:
                success, img = cap.read()
                # 在每一帧上添加字幕文本
                img_handle = write_text(img, text[q_flag])
                # 写入视频
                out.write(img_handle)
                flag += 1

            q_flag+=1
            if q_flag==num_data_handle.shape[0]:
                break
            global_flag+=lasting

        else:
            success, img = cap.read()
            out.write(img)
            global_flag+=1






#将合成的视频和音频进行合并（输入视频路径后分离出的音频   写入文字后的视频）
def combine_audio_video(output_path,audio_path='./../media/file_audio.mp3',video_path='./../media/video_done.avi'):
    video=VideoFileClip(video_path)
    audio=AudioFileClip(audio_path)
    final_video=video.set_audio(audio)#
    final_video.write_videofile(output_path)

# print(get_video_info('./../media/test_video.mp4'))
# l=read_lines()
# put_text_on_each_frame(framerate=25,
#                        frame_num=2262,
#                        width=1920,
#                        height=1080,
#                        num_data=num_data,
#                        text=l,
#                        to_bottem=90,
#                        input_video_path='./../media/test_video.mp4'
#                        )
#
# combine_audio_video(output_path='a.mp4')
# get_audio(input_video_path='./../media/test_video.mp4')
