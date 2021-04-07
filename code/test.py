import numpy as np
a=[0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0]
count=0
_data=np.asarray(a)
print(_data)
for j in range(len(_data)):
    if abs(_data[j])==0:
        if count == 0:
            print(j)
            count = 1
    else:
        if count == 1:
            print(j)
            count = 0