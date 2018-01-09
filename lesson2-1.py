# !usr/bin/python3
# -*- coding:UTF-8 -*-

# 课程2-1---如何在列表，字典，集合中根据条件筛选数据？

# 案例1：过滤掉列表中的负数

# 方法一：迭代

from random import randint

data = [randint(-10, 10) for _ in range(10)]
print(data)

res = []
for a in data:
    if a >= 0:
        res.append(a)

print(res)

# 方法二：filter函数  filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表。
# 该接收两个参数，第一个为函数，第二个为序列，序列的每个元素作为参数传递给函数进行判，然后返回 True 或 False，
# 最后将返回 True 的元素放到新列表中

print(list(filter(lambda x: x >= 0, data)))

# 方法三：列表解析， 3个方法中效率最高，推荐使用。

print([x for x in data if x >= 0])

# 案例2：筛选出字典中高于值高于90的项

d = {x: randint(0, 101) for x in range(1, 21)}
print(d)
print({k: v for k, v in d.items() if v > 90})

# 案例3：筛选出集合中能被3整除的数

s = set(data)
print({x for x in s if x % 3 == 0})
