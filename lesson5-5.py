#!usr/bin/python3
# -*- coding: UTF-8 -*-

# lesson5-5 如何访问文件的状态

# 案例：在某些项目中，我们需要获得文件状态，例如：
# 1.文件的类型（普通文件，目录，符号链接，……）
# 2.文件的访问权限
# 3.文件的最后访问、修改、节点状态更改时间
# 普通文件的大小

# 方案一：系统调用，利用标准库中OS模块下的三个系统调用stat,fstat,lstat获取文件状态

import os
import stat
import time


print('根目录下有以下文件：', os.listdir('.'))
print('以test.py为例，获取他的文件状态')

s = os.stat('test.py')
print('test.py是否是普通文件？', stat.S_ISREG(s.st_mode))  # 检查是否是普通文件
print('test.py是否是目录？', stat.S_ISDIR(s.st_mode))  # 检查是否是目录
print('test.py是否是链接文件？', stat.S_ISLNK(s.st_mode))  # 检查是否是链接文件

print('test.py是否有读权限', bool(s.st_mode & stat.S_IRUSR))  # 检查是否有读权限
print('test.py是否有执行权限', bool(s.st_mode & stat.S_IXUSR))  # 检查是否有执行权限

print('test.py的最后访问时间是', time.localtime(s.st_atime))
print('test.py的最后修改时间是', time.localtime(s.st_mtime))
print('test.py的最后节点更新时间是', time.localtime(s.st_ctime))

print('test.py的文件大小是', s.st_size)

# 方案二：使用os.path函数，简洁调用. 但这个函数没有验证权限的功能

print('-' * 30, '以下是方案二', '-' * 30)

print('test.py是否是普通文件？', os.path.isfile('test.py'))  # 检查是否是普通文件
print('test.py是否是目录？', os.path.isdir('test.py'))  # 检查是否是目录
print('test.py是否是链接文件？', os.path.islink('test.py'))  # 检查是否是链接文件

print('test.py的最后访问时间是', time.localtime(os.path.getatime('test.py')))
print('test.py的最后修改时间是', time.localtime(os.path.getmtime('test.py')))
print('test.py的最后节点更新时间是', time.localtime(os.path.getctime('test.py')))

print('test.py的文件大小是', os.path.getsize('test.py'))

# 课后小结&拓展
#     1.linux的链接文件相当于Windows下的文件快捷方式
#     2.文件的类型信息和权限信息都在stat的st_mode里面
#     3.使用os.path可以方便快捷地访问文件状态