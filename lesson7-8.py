#!usr/bin/python3
# -*- coding: UTF-8 -*-

'''
lesson7-8---如何通过实例方法名字的字符串调用方法？

案例：某项目中，我们的代码使用了三个不同的图形类：Circle，Triangle，Rectangle
他们都有一个获取图形面积的接口（方法），但接口名字不同。我们可以实现一个统一的获取面积的函数，使用每种方法名进行尝试
调用相应类的接口。

方案一：使用内置函数getattr，通过名字在实例上获取方法对象，然后调用

方案二：使用标准库operator下的methodcaller函数调用
'''


# 定义三个图形类
class Circle(object):
    def __init__(self, r):
        self.r = r

    def area(self):
        return self.r ** 2 * 3.14


class Rectangle(object):
    def __init__(self, h, w):
        self.h = h
        self.w = w

    def get_area(self):
        return self.h * self.w


class Triangle(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def getArea(self):
        a, b, c = self.a, self.b, self.c
        p = (a + b + c) / 2
        area = (p * (p - a) * (p - b) * (p - c)) ** 0.5
        return area


# 方案一
def getarea1(shape):
    for name in ('area', 'get_area', 'getArea'):
        f = getattr(shape, name, None)
        if f:
            return f()


# 方案二
from operator import methodcaller


def getarea2(shape):
    for name in ('area', 'get_area', 'getArea'):
        f = getattr(shape, name, None)
        if f:
            return methodcaller(name)(shape)


shape1 = Circle(2)
shape2 = Rectangle(3, 4)
shape3 = Triangle(3, 4, 5)
shape = [shape1, shape2, shape3]
print('调用方案一的函数：', list(map(getarea1, shape)))
print('调用方案二的函数：', list(map(getarea2, shape)))

'''
课后小结&拓展
    1.getattr(object,name,[,default])
    从类对象中查找方法名为字符串name的方法，并返回该方法：object.name，如果方法不存在，则返回default
    2.operator.methodcaller(name[,arge...])
    利用函数名或方法名称调用方法
    f = methodcaller('name', 'foo', bar=1) 调用f(b) , 返回 b.name('foo', bar=1)
'''