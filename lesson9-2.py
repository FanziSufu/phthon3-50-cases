#!usr/bin/python3
# -*- coding: UTF-8 -*-

'''
lesson9-2---如何为被装饰的函数保存元数据

案例：在函数对象中保存着一些函数的元数据，例如：
f.__name__ : 函数的名字
f.__doc__ ： 函数的文档字符串
f.__dict__: 属性字典
...
我们在使用装饰器后，再使用上面这些属性访问时，看到的是内部包裹函数的元数据，原来函数的元数据便丢失掉了，应该如何解决？

方案：使用标准库functools中的装饰器wraps装饰内部包裹函数，可以指定将原函数的某些属性，更新到包裹函数上面。
'''

from functools import update_wrapper, wraps


def mydecoctor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        '''wrapper.__doc__'''  # 文档属性
        print('In wrapper')
        print(func.__name__)
        func(*args, **kwargs)
        update_wrapper(wrapper, func)  # 使用update_wrapper 函数
    return wrapper


@mydecoctor
def example():
    '''example.__doc__'''
    print('In example')


print(example.__name__)
print(example.__doc__)
example()

'''
课后小结&拓展：
    1.update_wrapper(wrapper,wrapped,assigned = WRAPPER_ASSIGNMENTS,updated = WRAPPER_UPDATES)
    wrapper是包裹函数，wrapped是被包裹函数，assigned是用于替换的属性值，updated是用于更新合并的属性值
    2.wraps(wrapped,assigned = WRAPPER_ASSIGNMENTS, updated = WRAPPER_UPDATES)
    装饰器函数，放置于被装饰的包裹函数的上方，参数设置参考update_wrapper
'''
