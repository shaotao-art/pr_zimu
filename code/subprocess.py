# s='runas /user:starfish cmd'
#
# import subprocess
#
#
#
# echo = subprocess.Popen('python C:\\Users\starfish\pr_zimu\code\pawd.py',
#                         stdout=subprocess.PIPE,
#                         shell=False
#                         )
# # communicate 方法返回 输出到 标准输出 和 标准错误 的字节串内容
# # 标准输出设备和 标准错误设备 当前都是本终端设备
# outinfo, errinfo = echo.communicate()
#
# # 注意返回的内容是bytes 不是 str ，我的是中文windows，所以用gbk解码
# outinfo = outinfo
# errinfo = errinfo
# print (outinfo)
# print ('-------------')
# print (errinfo)
#
# sudo = subprocess.Popen(s,
#                         stdin=echo.stdout,
#                         stdout=subprocess.PIPE,
#                         )
#
#
# outinfo, errinfo = sudo.communicate()
#
# # 注意返回的内容是bytes 不是 str ，我的是中文windows，所以用gbk解码
# outinfo = outinfo.decode('gbk')
# errinfo = errinfo
# print (outinfo)
# print ('-------------')
# print (errinfo)
# a1 = subprocess.Popen('shaotao')
#
#
# outinfo, errinfo = a1.communicate()
#
# # 注意返回的内容是bytes 不是 str ，我的是中文windows，所以用gbk解码
# outinfo = outinfo.decode('gbk')
# errinfo = errinfo
# print (outinfo)
# print ('-------------')
# print (errinfo)
# a2 = subprocess.Popen('dir')

#
# outinfo, errinfo = a2.communicate()
#
# # 注意返回的内容是bytes 不是 str ，我的是中文windows，所以用gbk解码
# outinfo = outinfo.decode('gbk')
# errinfo = errinfo
# print (outinfo)
# print ('-------------')
# print (errinfo)
#
#





