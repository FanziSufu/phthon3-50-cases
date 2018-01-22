#!usr/bin/python3
# -*- coding: UTF-8 -*-

'''
lesson9-1---如何使用函数装饰器？

案例：某些时候，我们想为多个函数，统一添加某种功能，比如计时统计，记录日志，缓存运算结果等待。
比如，对于斐波那契数列和走台阶问题，我们需要维护代码以消除重复计算的问题，
我们不想在每个函数内一一添加完全相同的代码，有什么好的解决方案？

方案：定义装饰器函数，用它来生成一个在原函数基础添加了新功能的函数，替代原函数
'''


# 定义一个装饰器函数：
def memo(func):
    cache = {}

    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap


# 计算斐波那契数列第n项的值的函数,本例忽略对参数的判断
@memo
def fibonacci(n):
    if n <= 2:
        return 1
    return fibonacci(n - 2) + fibonacci(n - 1)


# 计算 对于 n个台阶，采用 每次走1~x步，即steps = range(1, x+1)，问有多少种走法
@memo
def climb(n, steps):
    count = 0
    if n == 0:
        count = 1
    elif n > 0:
        for step in steps:
            count += climb(n - step, steps)
    return count


if __name__ == '__main__':
    print('计算第50位斐波那契数列', fibonacci(50))
    print('计算10个台阶，每次走1~3步，共有几种走法：', climb(10, (1, 2, 3)))

'''
课后小结&拓展
    1.装饰器（Decorator）函数，本质是一个  返回函数的高阶函数。其作用是在不修改原函数的基础上，动态地为函数增加
    功能。利用装饰器，可以批量地给许多不同的函数增加相同的功能，从而避免了代码的复写，提高了效率。
    装饰器函数的传入参数为 函数名，其内部有一个内置函数，作为闭包，可以引用闭包外的变量
    2.把装饰器语法糖放在待装饰函数的上方，如本例中，@memo，在执行fibonacci（50）时， 相当于执行了 
    fibonacci = memo(fibonacci)
    fibonacci(50)
    这两条语句。在第一条语句里，程序调用了memo(finonacci)，根据该函数的定义，设置了全局变量cache = {}
    并返回一个 wrap 函数 ， 使变量 fibonacci 执行 wrap 函数
    执行第二条语句，相当于执行了 wrap(50)

'''