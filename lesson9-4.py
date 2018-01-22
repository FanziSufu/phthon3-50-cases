#!usr/bin/python3
# -*- coding: UTF-8 -*-

'''
lesson9-4---如何实现属性可修改的函数装饰器

案例：为分析程序内哪些函数执行时间开销较大，我们定义一个带timeout参数的函数装饰器，装饰功能如下：
1.统计被装饰函数单次调用运行时间
2.时间大于参数timeout的，将此次函数调用记录到log日志中
3.运行时可修改timeout的值

方案：为包裹函数增添一个函数，用来修改闭包中使用的自由变量
在python3中：使用nonlocal访问嵌套作用域中的变量引用
'''

import time
import logging
from random import randint


# 构建案例所需的装饰器
def warn(timeount):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)  # 执行func函数，并将结果返回给res
            used = time.time() - start
            if used > timeount:
                msg = '"%s:" %s > %s' % (func.__name__, used, timeount)
                logging.warning(msg)  # 调用日志
            return res

        def setTimeout(t):  # 为wrapper添加一个函数，用于改变需要修改的属性
            nonlocal timeount
            timeount = t
        wrapper.setTimeout = setTimeout  # 把这个函数设置为包裹函数wrapper的属性，方便修改
        return wrapper
    return decorator


@warn(1.5)
def test():
    print('In test')
    while randint(0, 1):
        time.sleep(0.5)


if __name__ == '__main__':

    for _ in range(30):
        test()

    test.setTimeout(1)
    print('-' * 30, '将timeout设置为1秒', '-' * 30)

    for _ in range(30):
        test()


'''
课后小结&拓展：
    1.我们要实现一个属性可修改的函数装饰器，需要在第二次decorator函数下，为包裹函数wrapper增添一个属性，
    这个属性是也是一个函数，用来修改闭包中的自由变量，在该函数中，用 nonloacl 访问整个嵌套作用域的变量引用
'''