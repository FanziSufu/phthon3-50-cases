# !usr/bin/python3
# -*- coding:UTF-8 -*-

# lesson4-1---如何拆分含有多种分隔符的字符串

# 案例：把某个字符串依据分隔符符号拆分不同的字段，该字符串包含多种不同的分隔符。
# 如s = 'ab;cd|efg|hi,jkl|mn\topq;rst,uvw\txyz',其中<,>,<;>,<|>,<\t>都是分隔符号，如何处理

# 方案一：连续使用str.split()方法，每次处理一种分隔符号.


def mySplit(s, ds):
    res = [s]

    for d in ds:
        t = []
        list(map(lambda x: t.extend(x.split(d)), res))
        res = t

    return [x for x in res if x]


s = 'ab;cd|efg|hi,jkl|mn\topq;rst,uvw\txyz'
print(mySplit(s, ',;|\t'))

# 方案二：使用正则表达式re.split()方法，一次性拆封字符串


import re

print('-' * 30, '方案二的结果', '-' * 30)
print(re.split(r'[,;|\t]+', s))


# 课后小结&拓展：
#     1.str.split()方法适用于处理单一分隔符，速度更快；re.split()适用于处理多个分隔符的情况
#     2.方案一较方案二，明显复杂，但方案一的解决思路值得学习，这里设计的map函数，list.extend()方法的组合运用
#     3.map函数在python2和python3中有所不同，前者返回列表，在程序中写出，就会执行作为参数的函数；
#     但在python3中，返回的是一个迭代器，单单写一行map函数，是不执行作为参数的函数的，只有用到的时候才执行，比如
#     使用list括起来，这样就返回一个列表，同是参数函数也会被执行。  这种改动，有利于节省内存
#     4.re.split(pattern,string,maxsplit=0,flags=0)
#     位于re模块，用pattern（正则表达式）分隔字符串，返回分隔后字符串的列表，如果用括号讲pattern括起来，则还会返回
#     分隔符
#     5.[;,|\t]+ 是正则表达式的写法，意思是至少含有中括号内一个分隔符