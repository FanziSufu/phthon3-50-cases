# !usr/bin/python3
# -*- coding:UTF-8 -*-

# lesson5-1---如何读写文本文件

# 案例：某文本文件编码格式已知（如UTF-8,GBK,BIG5)
# 在python2和python3中分别如何读取该文件？

# 方案：在python2中，写入文件前对unicode编码，读入文件后对二进制字符串编码
#      在python3中，open函数指定't'的文本模式，用endcoding指定编码格式

# python2

# f = open('py2.txt', 'w')
# s = u'你好'
# f.write(s.encode('gbk'))
# f.close()
# f = open('py2.txt', 'r')
# t = f.read()
# print(t.decode('gbk'))

# python3

f = open('py3.txt', 'wt', encoding='utf8')
s = '你好'
f.write(s)
f.close()
f = open('py3.txt', 'rt', encoding='utf8')
t = f.read()
print(t)

# 课后小结&拓展
#     1.从python2到python3，字符串的语义发生了变化：str->bytes  unicod->str，因此，python3中读写文件时，不需要再对
#     字符串进行解码和编码
#     2.open（file, mode='r', buffering=-1, encoding=None,errors=None,newline=None, closefd=True, opener=None)
#     open函数参数很多，重点关注file和mode，file指文件名（若非同目录，需要加路径），mode指打开模式。默认是r，只读模式
#     'rt'表示打开以只读模式打开文本文件,'rb'表示以只读模式打开二进制文件。如r后面不接字符，则默认为'rt'