# !usr/bin/python3
# -*- coding: UTF-8 -*-

# lesson3-3---如何使用生成器函数实现可迭代对象

# 案例：实现一个可迭代对象的类，它能迭代出给定范围内所有素数

# 方案：将该类的__iter__方法实现生成器函数，每次yield返回一个素数


class PrimeNumbers:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def isPrimeNumber(self, k):
        if k < 2:
            return False
        for i in range(2, k):
            if k % i == 0:
                return False
        return True

    def __iter__(self):
        for k in range(self.start, self.end + 1):
            if self.isPrimeNumber(k):
                yield k


for x in PrimeNumbers(1, 20):
    print(x)

# 课后小结&拓展：
#     1.生成器：
#         在Python中，使用了yield的函数被称为生成器（generator）
#         跟普通函数不同的是，生成器是一个返回迭代器的函数，只能用于迭代操作，更简单地理解，生成器就是一个迭代器。
#         在调用生成器运行的过程中，每次遇到yield时函数会暂停并保存当前所有的运行信息，返回yield的值，并在下一次执行
#         next（）方法时从当前位置继续运行。
#     2.3-1&2的案例可以用yield实现，但3-3的案例却不能用Iterable、Iterator实现（因为__next__方法的机制），且
#     使用yield的代码更简洁，推荐使用。

