
#return 1,actual_lst,match_len_lst
def match(actual_lst,cal_lst,match_len_lst=[]):
    #结果 每段匹配的cal_lst中元素个数
    #匹配部分
    if len(cal_lst)>=len(actual_lst):
        current_pos=0  #当前匹配位置
        for each in actual_lst:
            temp_cha_lst=[]   #存储切边值与实际值误差的列表
            for i in range(0,len(cal_lst)-current_pos):
                temp_cha_lst.append(abs(sum(cal_lst[current_pos:current_pos+1+i])-each))  #计算切片与实际值误差的绝对值
            #找出最小值 并 更新current_pos
            minimum=min(temp_cha_lst)
            #误差合理情况
            if minimum<=3:
                match_len=temp_cha_lst.index(minimum)+1
                current_pos+=match_len
                match_len_lst.append(match_len)
            else:
                #误差不合理就（实在的确人工光看波形图也很难判别的话就一次性匹配多句话）
                #一次性匹配多个act语句  actual=[3, 8, 6]  -->  actual=[3,14]
                res=0
                hebing=2
                while res==0:
                    print('match does not prefect')
                    actual_lst=he_bing(actual_lst,current_pos,hebing)
                    res=match(actual_lst,cal_lst)[0]
                    hebing+=1
                return 1,actual_lst,match_len_lst
    else:
        print('the cal_lst is too short')
        return 0,actual_lst,match_len_lst
    #结果修正部分
    # 如果恰好匹配数相同 匹配是否成功
    if len(match_len_lst)==len(actual_lst):
        print('match prefect')
        return 1,actual_lst,match_len_lst
    else:

        return 0,actual_lst,match_len_lst



def he_bing(actual_lst,current_pos,hebing):

    #current_pos=1  开始位置的下标
    #hebing=2    联同 current_pos位一共要合并的数字个数
    actual_lst[current_pos]=sum(actual_lst[current_pos:current_pos+hebing])
    for i in range(0,hebing-1):
        del actual_lst[current_pos+1]
    return actual_lst


# return start_time_point,end_time_point
def make_time_point(old_act_lst,new_actual_lst,start_lst,end_lst,match_len_lst):
    start_time_point = []
    end_time_point = []
    for i in range(0, len(match_len_lst)):
        end = sum(match_len_lst[0:i + 1])
        start = end - match_len_lst[i]
        end_time_point.append((end_lst[end] - start_lst[end]) / 2 + start_lst[end] - 0.01)
        start_time_point.append(end_lst[start] - (end_lst[start] - start_lst[start]) / 2 + 0.01)

    #对极端的实在匹配不上 用多段文字匹配的进行修正
    res_compare=compare_old_new_actual_lst(old_act_lst,new_actual_lst)

    if res_compare==1:
        return start_time_point,end_time_point
    else:
        # 为了下面的插入操作更改start_lst值
        for i in range(0, len(res_compare[0])):
            res_compare[0][i] += sum(res_compare[1][0:i]) - i
        #插入空格
        for  i in range(0,len(res_compare[0])):
            for j in range(0, res_compare[1][i]-1):
                start_time_point.insert(res_compare[0][i] + 1 +i, ' ')
                end_time_point.insert(res_compare[0][i] + i, ' ')
        return start_time_point, end_time_point



def compare_old_new_actual_lst(old_act_lst,new_act_lst):
    start_lst=[]
    acumulate_num_lst=[]
    if len(old_act_lst)==len(new_act_lst):
        return 1
    else:
        i=0
        while i<len(old_act_lst):
            if old_act_lst[i]!=new_act_lst[i]:
                start_lst.append(i)
                temp=i+2
                while sum(old_act_lst[i:temp])!=new_act_lst[i]:
                    temp+=1
                acumulate_num_lst.append(temp-i)
                for _ in range(0,temp-i-1):
                    new_act_lst.insert(0,0)
                i=temp
            else:
                i+=1
        return start_lst,acumulate_num_lst

#1,actual_lst,match_len_lst
def get_res(actual_lst,cal_lst):
    temp = match(actual_lst=actual_lst, cal_lst=cal_lst, match_len_lst=[])
    return match(actual_lst=temp[1], cal_lst=cal_lst, match_len_lst=[])





