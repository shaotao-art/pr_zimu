from moviepy.editor import *
import cv2

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
def get_audio(input_video_path,output_audio_path='./../media/origin_audio.mp3'):
    video = VideoFileClip(input_video_path)
    audio = video.audio
    audio.write_audiofile(output_audio_path)

def read_lines(text_path='./../docs/done.txt'):
    with open(text_path,'r',encoding='utf-8')as text:
        file=text.readlines()
    return file


#将视频的每一帧进行添加文字的处理，并保存图片
def put_text_on_each_frame(framerate,width,height,num_data,text,to_bottem,path):
    '''
    :param framerate: video fps
    :param width: framewidth
    :param height: frameheight
    :param num_data: 输入的带有时间序列的numpy数组   存储的是time in ms
    :param text: 读入的文本
    :param path: 读入的视频路径
    :return: None
    '''
    cap=cv2.VideoCapture(path)
    # 创建视频写入对象
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # 视频参数
    out = cv2.VideoWriter('./../media/video_done.avi', fourcc, framerate, (width, height), True)

    for i in range(len(text)):
        #计算每一句字幕的 开始帧与最后帧
        # 输入是：time in ms
        # output：which
        # frame
        start_frame=int((num_data[i][0])/1000*framerate)
        end_frame=int((num_data[i][1])/1000*framerate)
        #持续的帧数
        lasting=end_frame-start_frame
        #跳转到开始帧
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)  # 设置要获取的帧号
        flag=0
        #遍历其中的每一帧
        while flag<lasting:
            success, img = cap.read()
            # 在每一帧上添加字幕文本
            retval, baseLine = cv2.getTextSize(text=text[i], fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1,
                                               thickness=1)  # fontFace=, fontScale=, thickness=
            print(retval, baseLine)
            img_handle = cv2.putText(img=img, text=text[i],
                                   org=(int((width - retval[0]) / 2), int(height - retval[1] - to_bottem)),
                                   fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1, color=(255, 255, 255),
                                   thickness=2, lineType=None, bottomLeftOrigin=None)
            #写入视频
            out.write(img_handle)
            flag += 1



#将合成的视频和音频进行合并（输入视频路径后分离出的音频   写入文字后的视频）
def combine_audio_video(output_path,audio_path='./../media/file_audio.mp3',video_path='./../media/video_done.avi'):
    video=VideoFileClip(video_path)
    audio=AudioFileClip(audio_path)
    final_video=video.set_audio(audio)#
    final_video.write_videofile(output_path)