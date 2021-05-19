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
a=[-1,2,3,4]
b=[1,2,3,4]

print(list(map(abs,a)))