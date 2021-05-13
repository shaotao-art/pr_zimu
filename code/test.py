class B:
    def __init__(self,msg):
        msg['a']='b'
class A:
    def __init__(self):
        self.num_in_A=dict()
        b=B(self.num_in_A)
        print(self.num_in_A)
a=A()
'''
A类中生成B类
现在 我要在B类中改A类的值

'''
a=[1,2,3,4]
b=[1,2,3,4]

print(a,b)
start=1
acc=3
for i in range(0,acc-1):
    a.insert(start+1+i,' ')
    b.insert(start  + i, ' ')

print(a,b)

