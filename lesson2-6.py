# !usr/bin/python3
# -*- coding:UTF-8 -*-

# lesson2-6---如何让字典保持有序

# 案例：某编程竞赛系统，对参赛选手编程解题进行计时，选手完成题目后，把该选手解题用时记录到字典中，以便赛后按选手名查询成绩。
# 答题用时越短，成绩越优。 比赛结束后，需按排名顺序依次打印选手成绩，如何实现？

# 方案：以collections.OrderedDict替代内置字典Dict，依次将选手成绩录入OrderedDict


from collections import OrderedDict
from random import randint
from time import time

d = OrderedDict()  # 定义最终存放的OrderedDict
players = list('ABCDEFG')  # 假定有7名参赛者
start = time()  # 模拟考试开始时间

for i in range(7):
    input()  # 模拟答题结束
    p = players.pop(randint(0, 6-i))  # 模拟答题结束的考生
    end = time()  # 模拟答题结束时间
    print(p, i+1, end - start)
    d[p] = (i+1, end - start)  # 依次给d赋值

print('-' * 20)  # 分隔符

for k in d:
    print(k, d[k])
