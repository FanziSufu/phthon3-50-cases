# !usr/bin/python3
# -*- coding:UTF-8 -*-

# lesson2-5---如何快速找到多个字典中的公共键（key)？

# 案例：对球员-进球数的N个字典，统计前N轮，每轮都有进球的球员

# 生成3个题设字典


from random import randint, sample

s1 = {x: randint(1, 4) for x in sample('abcdefg', randint(2, 6))}
s2 = {x: randint(1, 4) for x in sample('abcdefg', randint(2, 6))}
s3 = {x: randint(1, 4) for x in sample('abcdefg', randint(2, 6))}

print(s1)
print(s2)
print(s3)

# 方案一：利用for循环找键值相同的字典


res = []
for k in s1:
    if k in s2 and k in s3:
        res.append(k)
print('方案一，每场都有进球的球员是：', res)

# 方案二：把字典的键值转换为集合，利用集合的&找相同的键值


print('方案二，每场都有进球的球员是：', set(s1) & set(s2) & set(s3))

# 方案三：利用map函数和reduce函数，查找相同的键值

from functools import reduce
print('方案三，每场都有进球的球员是：', reduce(lambda a, b: a & b, map(set, [s1, s2, s3])))

