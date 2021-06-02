from moviepy.editor import *
import cv2

'''
震惊
opencv2竟然不支持中文文字写入图片
'''



def get_video_info(path):
    '''
    获取视频信息
    :param path:  输入视频路径
    :return: width, height, frame_nums, framerate 视频的宽 高 帧数 帧率
    '''
    #获取视频信息
    cap=cv2.VideoCapture(path)
    width=int(cap.get(3))
    height=int(cap.get(4))
    framerate=int(cap.get(5))
    frame_nums=int(cap.get(7))

    #截取视频中的一帧作为字幕样式时的显示图片
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(frame_nums/2))
    success, img=cap.read()
    cv2.imwrite('./../temp/one_frame.png', img)

    return width, height, frame_nums, framerate




def get_audio(input_video_path,output_audio_path='./../temp/audio_extract.wav'):
    '''
    #分离音频保存到./../media/audio_extract.mp3
    :param input_video_path:  输入视频路径
    :param output_audio_path:   输出音频路径
    :return:
    '''
    # 播放视频时（获得视频路径时）预先将视频和音频分离  取得音频文件
    video = VideoFileClip(input_video_path)
    audio = video.audio
    audio.write_audiofile(output_audio_path)


#
#
# def _write_text(img,each_line,width,height):
#     '''
#     在图片中写入文本
#     :param img:  图片
#     :param each_line:  文本
#     :param width: 图片的宽
#     :param height: 图片的高
#     :return: 生成的图片对象
#     '''
#     #将cv2图片转成pillow格式
#     img_pillow=Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     #创建对象
#     draw = ImageDraw.Draw(img_pillow)
#     # 字体大小
#     ttf_font = ImageFont.truetype('simhei.ttf', 45)
#     #获得字幕文本的大小
#     (zimu_x, zimu_y) = draw.textsize(text=each_line, font=ttf_font)
#     to_bottem=90
#     color=[255,255,255]
#     draw.text(xy=(int((width - zimu_x) / 2) ,int(height - zimu_y - to_bottem) ),
#               text=each_line,
#               fill=(color[0],color[1],color[2]),
#               font=ttf_font)  # 文字位置，内容，字体
#
#     img_done = cv2.cvtColor(np.asarray(img_pillow), cv2.COLOR_RGB2BGR)
#
#     return img_done
#
#
#
#
# def put_text_on_each_frame(framerate,frame_num,width,height,num_data,text,input_video_path):
#     '''
#     #将视频的每一帧进行添加文字的处理，并保存图片
#     :param framerate: video fps
#     :param width: framewidth
#     :param height: frameheight
#     :param num_data: 输入的带有时间序列的numpy数组   存储的是time in ms
#     :param text: 读入的文本
#     :param path: 读入的视频路径
#     :return: None
#     '''
#     num_data_handle = num_data / 1000 * framerate
#     cap=cv2.VideoCapture(input_video_path)
#     # 创建视频写入对象
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     # 视频参数
#     out = cv2.VideoWriter('./../media/video_done.avi', fourcc, framerate, (width, height), True)
#
#     global_flag=0
#
#     q_flag=0
#
#     while global_flag<frame_num:
#         if global_flag==int(num_data_handle[q_flag][0]):
#
#             # 持续的帧数
#             lasting = int(num_data_handle[q_flag][1]) - int(num_data_handle[q_flag][0])
#             flag = 0
#             # 遍历其中的每一帧
#             while flag < lasting:
#                 success, img = cap.read()
#                 # 在每一帧上添加字幕文本
#                 img_handle = write_text(img, text[q_flag])
#                 # 写入视频
#                 out.write(img_handle)
#                 flag += 1
#
#             q_flag+=1
#             if q_flag==num_data_handle.shape[0]:
#                 break
#             global_flag+=lasting
#
#         else:
#             success, img = cap.read()
#             out.write(img)
#             global_flag+=1
#
#
#
#
#
#
#
# def combine_audio_video(output_path,audio_path='./../media/file_audio.mp3',video_path='./../media/video_done.avi'):
#     '''
#     #将合成的视频和音频进行合并（输入视频路径后分离出的音频   写入文字后的视频）
#     :param output_path: 输出视频的路径
#     :param audio_path: 输入音频路径
#     :param video_path: 输入无声 写过文本后 视频的路径
#     :return:
#     '''
#     video=VideoFileClip(video_path)
#     audio=AudioFileClip(audio_path)
#     final_video=video.set_audio(audio)#
#     final_video.write_videofile(output_path)

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
