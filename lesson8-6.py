#!usr/bin/python3
# -*- coding: UTF-8 -*-

'''
lesson8-6---如何使用多进程？

案例：由于python中全局解释器锁（GIL）的存在，在任意时刻只允许一个线程在解释器中运行。因此python的多线程不适合处理
cpu密集型的任务
想要处理cpu密集型的任务，可以使用多进程模型。

方案：使用标准库中multiprocessing.Process,它可以启动子进程执行任务，操作接口，进程间通信，进程间同步等
与Threading.Thread类型。 本结利用寻找阿姆斯特朗数来比较两种方案的运行效率
'''

from threading import Thread
from multiprocessing import Process


# 判断一个数是否为阿姆斯特朗数
def isArmstrong(n):
    a, t = [], n
    while t > 0:  # 把n拆成由各位数字组成的序列
        a.append(t % 10)
        t //= 10
    k = len(a)
    return sum(x ** k for x in a) == n


# 寻找给定范围内的阿姆斯特朗数
def findArmstrong(a, b):
    print(a, b)
    res = [x for x in range(a, b) if isArmstrong(x)]
    print('%s ~ %s: %s' % (a, b, res))


# 使用多线程寻找
def findbyThread(*argslist):  # 设置可以传入多组参数
    workers = []
    for args in argslist:
        worker = Thread(target=findArmstrong, args=args)
        workers.append(worker)
        worker.start()

    for worker in workers:
        worker.join()


# 使用多进程寻找
def findbyProcess(*argslist):  # 设置可以传入多组参数
    workers = []
    for args in argslist:
        worker = Process(target=findArmstrong, args=args)
        workers.append(worker)
        worker.start()

    for worker in workers:
        worker.join()


if __name__ == '__main__':
    import time
    start = time.time()
    findbyThread((20000000, 25000000), (25000000, 30000000))
    print('使用线程用时：', time.time() - start)

    start = time.time()
    findbyProcess((20000000, 25000000), (25000000, 30000000))
    print('使用进程用时：', time.time() - start)

'''
课后小结&拓展：
    1.使用多进程Process的操作和使用Thread的操作非常像，对于CPU密集型的程序，使用多进程Process可以有效提高效率。
    本机是单核系统，测试发现仍可以节省一半时间。
    2.多线程的通信，我们可以使用queue下的Queue， 而多进程的通信，可以调用multiprocessing下的Queue和Pipe
'''