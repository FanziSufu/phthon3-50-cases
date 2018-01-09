# !usr/bin/python3
# -*- coding:UTF-8 -*-

# lesson4-6---如何去掉字符串中不需要的字符？

# 案例1：过滤掉用户输入中前后多去的空白字符 '    nick2008@gmail.com    '

# 方案：str.strip,lstrip,rstrip去掉两端的字符

s1 = '    nick2008@gmail.com    '

print('去掉两端的空白字符串：', s1.strip())
print('去掉左边的空白字符串：', s1.lstrip())
print('去掉右边的空白字符串：', s1.rstrip())

# 案例2：删除单个固定位置的字符

# 方案：可以使用切片+拼接的方式

s2 = 'abc+123'  # 要求删除‘+’

print('使用切片+拼接的方式删除固定位置的字符：', s2[:3] + s2[4:])

# 案例3：删除任意位置字符

# 方案一：使用str.replace方法，用''替换待删除字符

s3 = '\tabc\t123\txyz'

print('使用str.replace方法删除指定字符串：', s3.replace('\t', ''))

# 方案二：使用re.sub方法，删除多个指定字符串

import re


s4 = '\tabc\n123\rxyz'

print('使用re.sub方法，删除多个指定字符串：', re.sub('[\t\n\r]', '', s4))

# 案例4：给字符串'\tabc\n123\rxyz'加密,并删除\t\n\r

# 方案：使用str.translate方法，将abc转换为xyz , 将xyz装换为abc

s5 = '\tabc\n123\rxyz'
print('使用str.translate方法转换字符串：', s5.translate(str.maketrans('abcxyz', 'xyzabc', '\t\n\r')))

# 课后小结&拓展:
#     1.str.strip([chars])
#     去除字符串左右两端的字符串，可以同时去除所有chars中的所有字符。如果不传入参数，则去除两端空白字符
#     2.str.replace(old, new,[, count])
#     替换连续的字符串，如果要替换的字符串是分散的，就不好使用这个方法了
#     3.str.translate(table)
#     在Python3中，该方法只接收一个参数了，不能使用（None, '')的技巧做删除操作。但可以通过对传入的table做处理，实现
#     删除操作。技巧是创建3个参数的str.maketrans('', '', '（要删除的字符放这里）'),前2个为空，把要删除的字符放入第三个参数的位置
