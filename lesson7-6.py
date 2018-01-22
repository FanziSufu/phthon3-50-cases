#!usr/bin/python3
# -*- coding: UTF-8 -*-

"""
lesson7-6---如何使用描述符对实例属性做类型检查

案例：在某项目中，我们实现了一些类，并希望能像静态类型语言那样对它们的实例属性做类型检查
p = Person()
p.name = 'Bob'  # str
p.age = 18  # int
p.height = 1.83  # float
要求：1.可以付实例变量名指定类型 2.赋予不正确类型时抛出异常

方案：使用描述符来实现需要类型检查的属性：分别实现__get__,__set__,__delete__方法，在__set__内使用
instance函数做类型检查
"""


# 创建一个判断属性类型的类（描述符）
class Attr(object):
    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_

    def __get__(self, instance, cla):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.type_):
            raise TypeError('expected type %s' % self.type_)
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


# 创建需要做属性检查的类（即需要实例化使用的类）
class Person(object):
    name = Attr('name', str)
    age = Attr('age', int)
    height = Attr('height', float)


p = Person()
p.name = 'Bob'
p.age = 18
p.height = 1.83
print('p.name = %s, p.age = %s, p.height = %s' % (p.name, p.age, p.height))
p.age = '18'  # 错误测试，提示错误信息

'''
课后小结&拓展：
    1.在python中，要实现对实例属性做类型检查，需要把待检查的属性封装到一个类中，在这个类中实现__get__,__set__
    __delete__方法，这个类便是描述符。
'''
