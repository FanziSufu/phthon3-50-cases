#!usr/bin/python3
# -*- coding: UTF-8 -*-

"""
lesson7-4---如何创建可管理的对象属性

案例：在面向对象编程中，我们把方法（函数）看作对象的接口。直接访问对象的属性可能是不安全的，或设计上不够灵活。
但是使用调用方法在形式上不如访问属性简洁。
circle.getRadius()
circle.setRadius(5.0) # 繁

circle.radius
circle.radius = 5.0  # 简
能否在形式上是属性访问，但实际上调用方法？

方案：使用property函数为类创建可管理属性，fget/fset/fdel对象相应属性访问.
"""


class Circle(object):
    def __init__(self, radius):
        self.radius = radius

    def getRadius(self):
        return self.radius

    def setRadius(self, new_radius):
        if not isinstance(new_radius, (int, float)):
            raise ValueError('Wrong type.')
        self.radius = float(new_radius)

    R = property(getRadius, setRadius)


c = Circle(3.2)
print('修改前',c.R)
c.R = 5.5
print('修改后',c.R)

'''
课后小结&拓展：
    1.property(fget=None, fset=None, fdel=None, doc=None)
    内建函数property()可以为类创建可管理属性。使之既具有调用方法的安全性，灵活性，又具有调用属性的简洁性.
'''