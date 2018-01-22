#!usr/bin/python3
# -*- coding: UTF-8 -*-

# 如何为创建大量实例节省内存

# 案例：某网络游戏中，定义了玩家类Player（uid,name,status,...)，每有一个在线玩家，在服务器程序内侧则有一个Player
# 的实例，当在线人数很多时，将产生大量实例（如百万级） 如何降低这些大量实例的内存开销？

# 方案：定义类的__slots__属性，它是用来声明实例属性名字的列表.


class Player1(object):
    def __init__(self, uid, name, status=0, level=1):
        self.uid = uid
        self.name = name
        self.status = status
        self.level = level


class Player2(object):
    __slots__ = ['uid', 'name', 'status', 'level']

    def __init__(self, uid, name, status, level):
        self.uid = uid
        self.name = name
        self.status = status
        self.level = level


p1 = Player1
p2 = Player2

print('Player1比Player2多出的方法是：', set(dir(p1)) - set(dir(p2)))  # 利用集合的加减运算

from sys import getsizeof  # 求对象的占用字节数

print('__dict__占用的内存是：', getsizeof(p1.__dict__))  # 在python2中，占用的是1048个字节，而python3是48个字节

# 课后小结&拓展：
#     1.把数组转换成集合，可以方便得进行加减运算，用于找出两个数组的差异
#     2.sys.getsizeof()可以返回对象占用的字节数
#     3，__slots__，其作用是阻止在实例化类时为实例分配dict，从而达到节省内存的目的。利用__slots__还可以限定类的属性。