#!usr/bin/python3
# -*- coding: UTF-8 -*-

# lesson7-1---如何派生内置不可变类型并修改实例化行为

# 案例：我们想自定义一种新类型的元组，对于传入的可迭代对象，我们只保留其中的int类型且值大于0的元素，
# 例如：IntTuple([1, -1, 'abc', 6, ['x', 'y'], 3] => (1,6,3)
# 要求IntTuple是内置tuple的子类，如何实现？

# 方案：定义类IntTuple继承内置tuple，并实现__new__，修改实例化行为


class IntTuple(tuple):
    def __new__(cls, iterable):
        g = (x for x in iterable if isinstance(x, int) and x > 0)
        return super(IntTuple, cls).__new__(cls, g)


t = IntTuple([1, -1, 'abc', 6, ['x', 'y'], 3])
print('调用IntTuple实例：', t)

# 课后小结&拓展：
#     1.__new__和__init__的区别
#     ①继承自object的新式类才有__new__
#     ②__new__至少要有一个参数cls，代表当前类，此参数在实例化时由python解释器自动识别
#     ③__new__必须要有返回值，返回实例化出来的实例。在自己实现__new__是要特别注意，可以return父类
#     （通过super(当前类名,cls)）__new__出来的实例，或者直接是object的__new__出来的实例
#     ④__init__有一个参数self，就是这个__new__返回的实例，__init__在__new__的基础上可以完成一些其他初始化动作
#     __init__不需要返回值
#     ⑤我们在使用时，尽量使用__init__函数，不要去自定义__new__函数。我们使用__new__，通常是在继承一些不可变的
#     类对象时，我们需要自定义实例化行为（如本例）。在python3，本例中，自定义了__new__后，不需要再自定义__init__
#     2.super()
#     ①super()不是一个函数，而是一个类名，形如super(B,self)事实上调用了super类的初始化函数，产生了一个super对象
#     ②super()机制是用来解决多重继承的，用于保证相同的基类只初始化一次
#     ③super()可以解决 用类名调用时，修改基类名称会导致大量修改派生类代码的问题。 最好使用super()继承基类方法。
#     ④super()只能用于新式类，无法用于经典类
#     新式类：必须有可以继承的类，如果无继承的类，则继承object
#     经典类：没有父类的类对象