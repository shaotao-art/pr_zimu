fileName_choose='/home/starfish/桌面/pr_zimu/docs/a.txt'

with open(fileName_choose, 'r')as f:
    a = f.readlines()
for each in a:
    print(each)