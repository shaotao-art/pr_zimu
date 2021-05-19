act=[[14, 22, 2, 18, 13, 6, 4, 16, 13, 11, 9, 9, 8, 16, 17, 4, 4, 4, 3, 9, 11, 6, 19],
     [6, 10, 4, 7, 10, 8, 5, 5, 8, 10],
     [9, 6, 4, 8, 19, 2, 13, 8, 15, 9, 13, 3, 9, 13, 6, 8, 9, 14, 4, 7, 6, 13, 6, 7, 7, 9],
     [6, 9, 2, 11, 14, 10, 14, 10, 10, 10, 10, 12, 7, 9, 17, 12, 13, 4, 18, 12],
     [9, 5, 5, 4, 7, 8, 6, 16, 10, 9, 7, 7, 17, 4, 13, 16],
     [3, 8, 6, 7, 9, 15, 15, 7, 9, 5, 14, 11, 12],
     [2, 26, 9, 17, 7, 17, 10, 4, 9, 6, 6, 6, 18, 8, 21, 22],
     [8, 7, 11, 18, 7, 7, 9]]
cal=[[3.3536284004753028, 5.5247273836188295, 6.544580796449941, 3.747804872919225, 11.174590155315098, 8.008664836955953, 1.8332334353344557, 5.143064449982645, 12.538565885359162, 7.896042987686267, 5.211888913425258, 5.987728319505343, 4.235832886421221, 6.90747342187452, 8.515463158669549, 14.859827334195604, 11.34352292921965, 8.953437016940564, 8.94092347813283, 6.882446344259034, 9.42895149163486, 8.803274551247691, 7.789677907820436, 8.515463158669549, 4.429792737941286, 4.442306276749018, 4.70509059171161, 2.834316539953967, 7.501866515242337, 9.347613489384514, 4.536157817807095, 2.7154379212803823, 11.82529417331777, 3.4850205579566014],
     [6.545338441890168, 8.6845466155811, 3.5440613026819934, 6.028097062579824, 8.499361430395911, 8.212005108556836, 5.574712643678156, 5.727969348659001, 8.652618135376752, 7.081736909323125, 4.4125159642400975],
     [10.092525835135788, 5.573206834021545, 4.3891328570492245, 7.631387778287565, 6.230336894540214, 7.5631950361582625, 6.664290708090275, 2.12017434620174, 6.230336894540214, 5.604203534989405, 6.788277511961725, 9.19362150706781, 4.717697887308561, 9.08823272377707, 13.458767560245578, 2.6595169430425307, 8.703873631775574, 12.16930479998254, 4.829286010792868, 8.393906622096985, 8.548890126936238, 13.95471477573136, 3.5584212711105074, 6.428715780734517, 7.036251119704648, 13.843126652247031, 6.732483450219583, 7.668583819449002, 7.315221428415361, 6.707686089445273, 3.074872736011881],
     [6.629458769256121, 4.8377131559436535, 4.794464123898183, 1.6002141856825103, 6.369964576983281, 4.553505231073401, 13.431913666694138, 9.29854188977675, 12.054123074388345, 5.177526979158078, 6.017793887470125, 4.479364033281155, 5.783013427794701, 6.22168218139881, 2.5331575912348567, 5.430842738281566, 4.294011038800555, 11.460993492050408, 6.654172501853508, 8.742482906334972, 10.81225801136835, 2.1500947359749407, 5.616195732762208, 10.36741082461485, 5.091028915067147, 9.378861520718333, 3.867699151495163, 4.819177856495595, 7.383227613477211, 5.813905593541503, 5.344344674190656, 3.323997034352059, 5.640909465359599],
     [9.59715928965971, 4.8392948660587125, 4.4554084944723265, 4.3972438927168165, 6.29340990994655, 7.7184426529566315, 5.118484954485176, 6.67147982135739, 1.8903495570541922, 7.648645130850019, 2.838432565669051, 7.561398228216749, 8.311721590862884, 6.979752210661609, 6.566783538197462, 13.942055040796559, 7.241492918561419, 3.7341674327039764, 10.172988847039326, 2.9314959284778674, 5.362776281858339, 8.695607962449241],
     [3.338151790860048, 2.9494628837051122, 5.710297327173268, 6.316194741267731, 7.105004582258627, 7.69946996967207, 11.294842360855235, 4.8528953260962036, 5.098683899738287, 2.7379703901061068, 6.470527101461585, 7.505125516094593, 8.191047116956247, 4.407046285536114, 8.288219343744972, 3.7096926579934433, 6.293330687905682, 5.881777727388674, 4.721427019264379, 2.995190990429227, 5.407348620126033],
     [2.6237713103215965, 11.088826593837606, 7.113586871518466, 6.231456862013788, 7.74691098090644, 8.73082522227703, 9.516825679463887, 7.6620907876848365, 10.031401518341617, 6.638593789477485, 4.908261847756789, 5.5415859571447434, 4.648146588543858, 10.698653705018241, 5.1627224274215795, 5.852593332290629, 6.304967696139155, 6.423715966649407, 6.078780514214892, 4.987427361430252, 6.94960116462337, 3.511555999374385, 4.21839094288772, 6.265384939302442, 7.515069119434046, 7.181443026095773, 14.334612654450961],
     [7.261067196978558, 7.1770918631661615, 4.529069670281922, 7.037132973478834, 3.364611708083361, 15.585821955580807, 6.6788382158792725, 6.606059593241861, 8.733434716489244]]



# return 1,actual_lst,match_len_lst
def match(actual_lst, cal_lst,duration_lst, match_len_lst=[]):
    # 结果 每段匹配的cal_lst中元素个数
    # 匹配部分
    if len(cal_lst) >= len(actual_lst):
        current_pos = 0  # 当前匹配位置
        for each in actual_lst:
            temp_cha_lst = []  # 存储切边值与实际值误差的列表
            for i in range(0, len(cal_lst) - current_pos):
                temp_cha_lst.append(sum(cal_lst[current_pos:current_pos + 1 + i]) - each)  # 计算切片与实际值误差的绝对值
            # list(map(abs, a))
            # 找出最小值 并 更新current_pos
            minimum = min(temp_cha_lst)
            _index=temp_cha_lst.index(minimum)
            match_len = temp_cha_lst.index(minimum) + 1  # 匹配的段数
            left=_index-1
            right=_index+1
            if minimum<1.5:
                pass
            else:
                if 0<=left<len(temp_cha_lst) and temp_cha_lst[left]<3:
                    res1=_choose(current_act_len=each,duration_lst=duration_lst,current_pos=current_pos,match_len=match_len,flag=0)
                    if res1[0]==0: #选择左边的概率更大
                        minimum=temp_cha_lst[left]
                if 0<=right<len(temp_cha_lst) and temp_cha_lst[right]<3:
                    res2=_choose(current_act_len=each,duration_lst=duration_lst,current_pos=current_pos,match_len=match_len,flag=1)
                    if res2[0]==0: #选择右边的概率更大
                        minimum=temp_cha_lst[right]
            # 误差合理情况
            if minimum <= 3:
                match_len = temp_cha_lst.index(minimum) + 1  # 匹配的段数
                current_pos += match_len  # current pos 更新
                match_len_lst.append(match_len)
            else:
                # 误差不合理就（实在的确人工光看波形图也很难判别的话就一次性匹配多句话）
                # 一次性匹配多个act语句  actual=[3, 8, 6]  -->  actual=[3,14]
                res = 0
                hebing = 2
                while res == 0:
                    print('match does not prefect')
                    actual_lst = he_bing(actual_lst, current_pos, hebing)
                    res = match(actual_lst, cal_lst)[0]
                    hebing += 1
                return 1, actual_lst, match_len_lst
    else:
        print('the cal_lst is too short')
        return 0, actual_lst, match_len_lst
    # 结果修正部分
    # 如果恰好匹配数相同 匹配是否成功
    if len(match_len_lst) == len(actual_lst):
        print('match prefect')
        return 1, actual_lst, match_len_lst
    else:

        return 0, actual_lst, match_len_lst


'''
当误差数组中 有两个小于三的怎么处理  即是出现了不确定的分法
需要考虑的因素：
    1 这一句的实际长度  如果是短句子  倾向与一次性匹配  长句子 趋向于匹配段数多的
    2 两句 之间间隔的大小  倾向匹配间隔大的   如果出现悬殊的则大致确定答案

'''
p_short_sentence_match_short = 0.8  # 短句子匹配少段数的概率
p_short_sentence_match_long = 0.2

p_long_sentence_match_short = 0.2  # 长句子匹配少段数的概率
p_long_sentence_match_long = 0.8

p_small_diffrent_in_duration_big = 0.55  # 两个间隔差不多 大间隔匹配的概率
p_small_diffrent_in_duration_small = 0.45
p_big_diffrent_in_duration_big = 0.9  # 两个间隔相差悬殊 大间隔匹配的概率
p_big_diffrent_in_duration_small = 0.1

param_judge_if_sentence_short = 12  # 判断句子是否短的参数

param_judge_if_duration_long = 0.2  # 判断间隔差别是否大的参数


def _choose(current_act_len, duration_lst, current_pos, match_len, flag):
    '''
    :param current_act_len: 当前匹配句子的实际长度
    :param duration_lst: 间隔持续时间的列表
    :param current_pos: 当前的匹配开始位置
    :param match_len: 当前的匹配匹配段数
    :param flag :判断是与左边的比较还是与右边的比较  flag==0 左边
    :return:
    '''

    p_choice1 = 0  # 选择 传进来初始值 的概率
    p_choice2 = 0  # 选择 传进来初始值 左边或右边 的概率

    #句子长短
    if current_act_len >= param_judge_if_sentence_short:  # 长句子
        if flag == 0:  # 与左边的选择比较
            p_choice1 += p_long_sentence_match_long
            p_choice2 += p_long_sentence_match_short
        if flag == 1:
            p_choice1 += p_long_sentence_match_short
            p_choice2 += p_long_sentence_match_long
    else:
        if flag == 0:  # 与左边的选择比较
            p_choice2 += p_short_sentence_match_short
            p_choice1 += p_short_sentence_match_long
        if flag == 1:
            p_choice1 += p_short_sentence_match_short
            p_choice2 += p_short_sentence_match_long

    #间隔大小
    if flag==0: #compare with the left
        if duration_lst[current_pos+match_len]<duration_lst[current_pos+match_len-1]:#左边的间隔更大
            if abs(duration_lst[current_pos+match_len]-duration_lst[current_pos+match_len-1])<param_judge_if_duration_long:#间隔相差不大
                p_choice2*=p_small_diffrent_in_duration_big
                p_choice1 *= p_small_diffrent_in_duration_small
            else:
                p_choice2 *= p_big_diffrent_in_duration_big
                p_choice1 *= p_big_diffrent_in_duration_small
    else:
        if duration_lst[current_pos+match_len]<duration_lst[current_pos+match_len+1]:#右边的间隔更大
            if abs(duration_lst[current_pos+match_len]-duration_lst[current_pos+match_len+1])<param_judge_if_duration_long:#间隔相差不大
                p_choice2*=p_small_diffrent_in_duration_big
                p_choice1 *= p_small_diffrent_in_duration_small
            else:
                p_choice2 *= p_big_diffrent_in_duration_big
                p_choice1 *= p_big_diffrent_in_duration_small

    if p_choice1>p_choice2:
        return 1,flag
    else:
        return 0,flag





def he_bing(actual_lst, current_pos, hebing):
    # current_pos=1  开始位置的下标
    # hebing=2    联同 current_pos位一共要合并的数字个数
    actual_lst[current_pos] = sum(actual_lst[current_pos:current_pos + hebing])
    for i in range(0, hebing - 1):
        del actual_lst[current_pos + 1]
    return actual_lst


# return start_time_point,end_time_point
def make_time_point(old_act_lst, new_actual_lst, start_lst, end_lst, match_len_lst):
    start_time_point = []
    end_time_point = []
    for i in range(0, len(match_len_lst)):
        end = sum(match_len_lst[0:i + 1])
        start = end - match_len_lst[i]
        end_time_point.append((end_lst[end] - start_lst[end]) / 2 + start_lst[end] - 0.01)
        start_time_point.append(end_lst[start] - (end_lst[start] - start_lst[start]) / 2 + 0.01)

    # 对极端的实在匹配不上 用多段文字匹配的进行修正
    res_compare = compare_old_new_actual_lst(old_act_lst, new_actual_lst)

    if res_compare == 1:
        return start_time_point, end_time_point
    else:
        # 为了下面的插入操作更改start_lst值
        for i in range(0, len(res_compare[0])):
            res_compare[0][i] += sum(res_compare[1][0:i]) - i
        # 插入空格
        for i in range(0, len(res_compare[0])):
            for j in range(0, res_compare[1][i] - 1):
                start_time_point.insert(res_compare[0][i] + 1 + i, ' ')
                end_time_point.insert(res_compare[0][i] + i, ' ')
        return start_time_point, end_time_point


def compare_old_new_actual_lst(old_act_lst, new_act_lst):
    start_lst = []
    acumulate_num_lst = []
    if len(old_act_lst) == len(new_act_lst):
        return 1
    else:
        i = 0
        while i < len(old_act_lst):
            if old_act_lst[i] != new_act_lst[i]:
                start_lst.append(i)
                temp = i + 2
                while sum(old_act_lst[i:temp]) != new_act_lst[i]:
                    temp += 1
                acumulate_num_lst.append(temp - i)
                for _ in range(0, temp - i - 1):
                    new_act_lst.insert(0, 0)
                i = temp
            else:
                i += 1
        return start_lst, acumulate_num_lst

def find_minimum_and_second_minimum(lst:list):
    minimium=min(lst)
    min_index=lst.index(minimium)
    if min_index==0:
        sec_min=lst[1]
        sec_min_index=1
    elif min_index==len(lst)-1:
        sec_min=lst[-2]
        sec_min_index=len(lst)-2
    else:
        sec_min=min(lst[min_index-1],lst[min_index+1])
        sec_min_index=lst.index(sec_min)
    return minimium,sec_min,min_index,sec_min_index

# lst=[0,1,2]
# print(sum(lst[0:2]))
# print(find_minimum_and_second_minimum(lst))
# lst=[2,1,0]
# print(find_minimum_and_second_minimum(lst))
# lst=[5,4,3,2,1,0,0.5,1]
# print(find_minimum_and_second_minimum(lst))

def match1(lst,sentence_len):
    minimium, sec_min,min_index,sec_min_index=find_minimum_and_second_minimum(lst)
    if sec_min>3:
        res=minimium
    else:
        if sentence_len<=12:
            if min_index<sec_min_index:
                res=minimium
            else:
                res = sec_min
            judge_pro_choice()
            pass
        else:
            if min_index==2:
                res=minimium
            else:
                res = sec_min
            judge_pro_choice()
            pass

def judge_pro_choice():
    pass

def my_fancy(current_pos,sentence_len,cal_lst):
    match_one=abs(sum(cal_lst[current_pos:current_pos+1])-sentence_len)
    match_two=abs(sum(cal_lst[current_pos:current_pos+2])-sentence_len)
    match_three=abs(sum(cal_lst[current_pos:current_pos+3])-sentence_len)
    minimum=min(match_three,match_two,match_one)
    if match_one==minimum:
        return 1
    elif match_two==minimum:
        return 2
    else:
        return 3
def my_fancy_main(cal_lst,act_lst):
    match_len_lst=[]
    current_pos=0
    for each_sentence_len in act_lst:
        match_len=my_fancy(current_pos,each_sentence_len,cal_lst)
        match_len_lst.append(match_len)
        current_pos+=match_len
    return match_len_lst

for i in  range(0,8):
    print(my_fancy_main(cal[i],act[i]))
'''
[3, 3, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2]
[1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
[1, 1, 1, 1, 3, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
[1, 2, 1, 2, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 3, 1, 2, 1, 3, 3]
[1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 2, 3]
[1, 2, 1, 1, 1, 2, 3, 1, 1, 1, 2, 2, 3]
[1, 3, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 3, 1, 3, 3]
[1, 1, 2, 2, 1, 1, 1]


001   最后的两个匹配出现问题
002   check
003   check
004   

'''


# 1,actual_lst,match_len_lst
def get_res(actual_lst, cal_lst,duration_lst):
    temp = match(actual_lst=actual_lst, cal_lst=cal_lst,duration_lst=duration_lst, match_len_lst=[])
    return match(actual_lst=temp[1], cal_lst=cal_lst,duration_lst=duration_lst, match_len_lst=[])
