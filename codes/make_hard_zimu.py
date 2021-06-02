from os.path import isfile
from moviepy.editor import (VideoFileClip,
                            TextClip,
                            CompositeVideoClip)


#读取srt文件
def read_srt(path):
    content = ""
    with open(path, 'r', encoding='UTF-8') as f:
        content = f.read()
        return content


# 取得文字
def get_sequences(content):
    sequences = content.split('\n\n')
    sequences = [sequence.split('\n') for sequence in sequences]

    sequences = [list(filter(None, sequence)) for sequence in sequences]

    return list(filter(None, sequences))


#时间转换
def strFloatTime(tempStr):
    xx = tempStr.split(':')
    hour = int(xx[0])
    minute = int(xx[1])
    second = int(xx[2].split(',')[0])
    minsecond = int(xx[2].split(',')[1])
    allTime = hour * 60 * 60 + minute * 60 + second + minsecond / 1000
    return allTime





class RealizeAddSubtitles():


    def __init__(self, videoFile, txtFile,save_path):
        self.src_video = videoFile
        self.sentences = txtFile
        if not (isfile(self.src_video) and self.src_video.endswith(('.avi', '.mp4')) and isfile(
                self.sentences) and self.sentences.endswith('.srt')):
            print('只支持.mp4 .avi 格式')
        else:
            video = VideoFileClip(self.src_video)

            w, h = video.w, video.h

            txts = []
            content = read_srt(self.sentences)
            sequences = get_sequences(content)

            for line in sequences:
                if len(line)<3:
                    continue
                sentences = line[2]
                start = line[1].split(' --> ')[0]
                end = line[1].split(' --> ')[1]

                start=strFloatTime(start)
                end=strFloatTime(end)

                start, end = map(float, (start, end))
                span=end-start
                txt = (TextClip(sentences, fontsize=20,font='SimHei', size=(w - 40, 40), align='center', color='white')
                       .set_position((10, h - 40))
                       .set_duration(span)
                       .set_start(start))

                txts.append(txt)

            video = CompositeVideoClip([video, *txts])

            video.write_videofile(save_path)


