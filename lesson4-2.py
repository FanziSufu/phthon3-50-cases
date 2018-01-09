# !usr/bin/python3
# -*- coding:UTF-8 -*-

# lesson4-2---如何判断字符串a是否以字符串b开头或结尾？

# 案例:某文件系统目录下有一系列文件：'d.java', 'c.h', 'g.sh', 'a.sh', 'e.py', 'b.py', 'f.cpp', 'h.c'
# 编写程序给其中所有.sh文件和.py文件加上用户可执行权限

# 方案：使用字符串的str.startswith()和str.endswith()方法。注意：匹配多个参数时，使用元组

import os
import stat


print('测试文件夹下有以下文件：', os.listdir('./test_file'))

res = [name for name in os.listdir('./test_file') if name.endswith(('.sh', '.py'))]

print('.sh文件和.py文件有：', res)

for x in res:
    print(x, '改动前文件的权限是：', oct(os.stat('./test_file/' + x).st_mode))
    os.chmod('./test_file/' + x, os.stat('./test_file/' + x).st_mode | stat.S_IXUSR)
    print(x, '改动后文件的权限是：', oct(os.stat('./test_file/' + x).st_mode))


# 课后小结&拓展：
#     1.str.startswith(str,beg=0,end=len(string))和str.endswith(str,beg=0,end=len(string))
#     这两个方法分别用于检索，给定范围内，被检查字符串是否以参数str开头或结尾。若是，则返回True，否则返回False
#     也可以传入元组作为检查参数，只要元组中的元素有一个检查成功，即返回True
#     2.在本结中，os模块用于操作系统文件，os.listdir()以列表形式返回目标路径下的文件名
#     os.stat()返回目标文件的状态信息，os.stat().st_mode返回目标文件的权限信息，利用oct()可以将权限信息的数字
#     转换为八进制，查看末三位数，即可确定目标文件的权限如何（文件的权限是由八进制标识的）
#     os.chmod()可以修改文件的权限。“ | stat.S_IXUSR ” 的含义是添加用户组权限。
