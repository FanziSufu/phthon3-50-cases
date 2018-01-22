#!usr/bin/python3
# -*- coding: UTF-8 -*-

'''
lesson9-5 如何在类中定义装饰器？

案例：实现一个能将函数调用信息记录到日志的装饰器：
1.把每次函数的调用时间，执行时间，调用次数写入日志
2.可以对被装饰函数分组，调用信息记录到不同日志
3.动态修改参数，比如日志格式
4.动态打开关闭日志输出功能

方案：为了让装饰器在使用上更加灵活，可以把类的实例方法作为装饰器
此时在包裹函数中就可以持有实例对象，便于修改属性和拓展功能
'''

import logging
from time import time, localtime, strftime, sleep
from random import choice


# 创建包含装饰器的类
class CallingInfo(object):
    def __init__(self, name):  # 传入name参数，实现不同组的调用信息记录到不同的日志
        logger = logging.getLogger(name)  # 传入name参数，实现不同组的调用信息记录到不同的日志
        logger.setLevel(logging.INFO)  # 创建一个名称为name的logger
        fh = logging.FileHandler(name + '.log')  # 设置logger的级别，低于级别的logger会被忽略
        logger.addHandler(fh)  # 创建一个名字为 name.log 的log文件
        logger.info('Start'.center(50, '-'))  # 把logger的内容写入到log文件中
        self.logger = logger
        self.logger.formatter = '%(func)s -> [%(time)s - %(used)s - %(ncalls)s'  # 设置写入日志的格式

    def info(self, func):
        def wrapper(*args, **kwargs):
            wrapper.ncalls += 1  # 每调用一次+1
            lt = localtime()  # 获取开始时的本地时间
            start = time()  # 记录开始时间
            res = func(*args, **kwargs)  # 执行func
            used = time() - start  # 得出调用时间
            info = {}  # 把所需信息记录在字典里
            info['func'] = func.__name__
            info['time'] = strftime('%x %X', lt)  # 转换时间格式，便于阅读
            info['used'] = used
            info['ncalls'] = wrapper.ncalls
            msg = self.logger.formatter % info  # 调用次数
            self.logger.info(msg)
            return res
        wrapper.ncalls = 0  # 在包裹函数外定义次数
        return wrapper

    def setformatter(self, formatter):
        self.logger.formatter = formatter  # 把记录格式设置成方法

    def turnon(self):
        self.logger.setLevel(logging.INFO)  # 调回级别，相当于打开了开关，又可以写入了

    def turnoff(self):
        self.logger.setLevel(logging.WARN)  # 提高logger的级别，这样一开始的logging.INFO级别的logger就会被忽略，从而实现控制开关的作用


if __name__ == '__main__':

    cainfo1 = CallingInfo('mylog1')
    cainfo2 = CallingInfo('mylog2')


    @cainfo1.info
    def f():
        print('in f')


    @cainfo1.info
    def g():
        print('in g')


    @cainfo2.info
    def h():
        print('in h')


    for _ in range(20):
        choice([f, g, h])()  # 随机选择一个函数执行
        sleep(choice([0.5, 1, 1.5]))  # 挂起0.5或1或1.5秒

    cainfo1.setformatter('%(func)s -> [%(time)s - %(ncalls)s')
    cainfo2.turnoff()
    print('-' * 30, '修改后', '-' * 30)

    for _ in range(20):
        choice([f, g, h])()
        sleep(choice([0.5, 1, 1.5]))

'''
课后小结&拓展：
    1.利用类的实例作为装饰器函数，非常便于修改属性，拓展功能
'''