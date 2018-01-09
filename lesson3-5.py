# !usr/bin/python3
# -*- coding:UTF-8 -*-

# lesson3-5---如何对迭代器做切片操作？

# 案例：对某个文本文件，我们想读取其中某范围的内容，如10~19行之间，python中文本文件是可迭代对象，我们是否可以使用类似
# 列表切片的方式得到一个10~19行文件内容的生成器？

# 方案一：使用readlines函数读取全部内容，再做列表的切片操作。  这种方法浪费内存，如果遇到大文件很可能导致内存不足。

f = open('/var/log/syslog')
lines = f.readlines()
for x in lines[9:19]:
    print(x)
f.seek(0)

print('-' * 30, '下面是方案二的结果', '-' * 30)

# 方案二：使用标准库中的itertools.islice，他能返回一个迭代对象切片的生成器

from itertools import islice


for x in islice(f, 9, 19):
    print(x)

print('-' * 30, '继续执行，返回原始文本第21行至24行的内容', '-' * 30)
for x in islice(f, 1, 5):
    print(x)

# 课后小结&拓展：
#     1.对于迭代器、生成器和文件，当我们对其进行遍历或者调用时，会同时改变其指针位置，例如，在执行上面的操作后，
#     文本指针已经指向了第20行，再执行最下面语句时，就返回从原始文本第21行至24行的内容
#     2.islice(iterable, [start,] stop [, step]) 函数：
#     位于itertools模块中，传入一个可迭代对象或迭代器对象，根据设定的索引范围，截取中间的元素。适用于获取大文件指定行数的内容