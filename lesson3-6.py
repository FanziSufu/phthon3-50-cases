# !usr/bin/python3
# -*- coding:UTF-8 -*-

# lesson3-6---如何在一个for语句中迭代多个可迭代对象？

# 案例一：某班学生末期考试成绩，语文，数学，英语分别存储在3个列表中，同时迭代三个列表，计算每个学生的总分。（并行）

# 方案：并行：使用内置函数zip，将多个可迭代对象合并，每次迭代返回一个元组。

from random import randint


chinese = [randint(60, 100) for _ in range(30)]
math = [randint(60, 100) for _ in range(30)]
english = [randint(60, 100) for _ in range(30)]

for c_score, m_score, e_score in zip(chinese, math, english):
    print('total score:', c_score + m_score + e_score)

# 案例二：某年级有4个班，某次考试每班英语成绩分别存储在4个列表中，依次迭代每个列表，统计全学年成绩高于90分的人数。

# 方案：串行，使用标准库中的itertools.chain，将多个可迭代对象链接起来。

from itertools import chain


e1 = [randint(60, 100) for _ in range(27)]
e2 = [randint(60, 100) for _ in range(29)]
e3 = [randint(60, 100) for _ in range(30)]
e4 = [randint(60, 100) for _ in range(24)]

count = 0
for score in chain(e1, e2, e3, e4):
    if score > 90:
        count += 1

print('4个班中成绩在90分以上的一共有%d人' % count)

课后小结&拓展：
    1.合并列表用zip函数，串联列表用itertools.chain函数
    2.zip（[iterable,...]）
    内置函数，用于将可迭代对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
    如果各个对象的元素个数不一致，则返回的列表长度与最短的对象相同。
    3.itertools.chain（[iterable,...]）
    位于itertools模块，将传入的列表，以串联的形式连接起来，返回一个迭代器。