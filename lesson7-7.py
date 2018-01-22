#!usr/bin/python3
# -*- coding: UTF-8 -*-

"""
lesson7-7---如何在环状数结构中管理内存

案例：在python中，垃圾回收器通过引用计数来回收垃圾对象，但某些环状数据机构（树，图……），存在对象间的循环引用，
比如树的父节点引用子节点，子节点也同时引用父节点。此时同时del掉引用的父子节点，两个对象不能被立即回收。
如何解决此类的内存管理问题？

方案：使用标准库weakref,它可以创建一种能访问对象但不增加引用技术的对象
"""

# 创建2个互相引用的类对象
import weakref


class Data(object):
    def __init__(self, value, owner):
        self.value = value
        self.owner = weakref.ref(owner)

    def __str__(self):
        return "%s's Data is %s" % (self.owner(), self.value)

    def __del__(self):
        print('in Data.__del__')


class Node(object):
    def __init__(self, value):
        self.data = Data(value, self)

    def __del__(self):
        print('in Node.__del__')


node = Node(100)
del node

'''在python3中，使用gc.collect()也能强制回收对象，而python2则不行
import gc
gc.collect()
'''

input('wait...')

'''
课后小结&拓展：
    1.weakref.ref(object[,callback])
    创建object的弱引用。跟通常的引用相比，它不占用计数器，如果一个对象只剩下一个弱引用，那么它可能被垃圾收集器收回。
    这个函数在解决循环引用的内存问题（如本例）有妙用，使可以使用del删除不需要的实例，及时释放内存。
    可选参数callback函数，在弱引用对象被销毁时调用。
'''