#!usr/bin/python3
# -*- coding: UTF-8 -*-

"""
lesson7-5---如何让类支持比较操作？

案例：有时我们希望自定义的类，实例间可以使用<,<=,>,>=,==,!=符号进行比较。例如，有一个矩形的类，
我们希望比较两个矩形的实例时，比较的是他们的面积。

方案：比较符号运算符重载，需要实现以下方法：
__lt__,__le__,__gt__,__ge__,__eq__,__ne__
使用标准库functools下的类装饰器total_ordering可以简化此过程
使用标准库abc下的abstractmethod，装饰一个基类的接口函数，可以简化同类型子类的定义。
"""

from abc import abstractmethod
from functools import total_ordering


# 创建基类
@total_ordering
class Shape(object):
    @abstractmethod
    def area(self):
        pass

    def __le__(self, obj):
        if not isinstance(obj, Shape):
            raise TypeError('obj is not Shape')
        return self.area() < obj.area()

    def __eq__(self, obj):
        return self.area() == obj.area()


class Rectangle(Shape):
    def __init__(self, h, w):
        self.h = h
        self.w = w

    def area(self):
        return self.w * self.h


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return self.r ** 2 * 3.14


r1 = Rectangle(3, 5)
r2 = Rectangle(4, 4)
c1 = Circle(3)

print('r1 > r2:', r1 > r2)
print('r1 < r2:', r1 < r2)
print('r1 <= r2:', r1 <= r2)
print('r1 >= r2:', r1 >= r2)
print('r1 == r2:', r1 == r2)
print('r1 != r2:', r1 != r2)
print('r1 > c1:', r1 > c1)
print('c1 > 1', c1 > 1)

'''
课后小结&拓展：
    1.function下的装饰器@total_ordering，是专门用于简化类创建中比较方法的创建过程的。其代价是占用了更多的栈道，运行效率会受到一定影响
    2.abc = Abstract Base Classes， 即抽象基础类。抽象类一般用作接口。
    3.装饰器@abstractmethod用于声明一个抽象方法，使该方法成为所有子类的接口。
'''
