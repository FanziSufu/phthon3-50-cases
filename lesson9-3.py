#!usr/bin/python3
# -*- coding: UTF-8 -*-

'''
lesson9-3---如何定义带参数的装饰器？

案例：实现一个装饰器，它用来检查被装饰函数的参数类型。装饰器可以通过参数指明函数参数的类型，调用时如果检测出
类型不匹配则抛出异常。

方案：带参数的装饰器，也就是根据参数定制化一个装饰器，可以看成是生产装饰器的工厂。
每次调用typeassert，返回一个特定的装饰器，然后用它区修饰其他函数
提取函数签名，可以使用 inspect.signature()
'''


from inspect import signature



def typeassert(*ty_args, **ty_kwargs):
    def decorator(func):
        sig = signature(func)
        btype = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        def wrapper(*args, **kwargs):
            for name, obj in sig.bind(*args, **kwargs).arguments.items():
                if name in btype:
                    if not isinstance(obj, btype[name]):
                        raise TypeError('"%s" must be "%s"' % (name, btype[name]))
            return func(*args, **kwargs)
        return wrapper
    return decorator


@typeassert(str, int, list)
def f(a, b, c):
    print(a, b, c)


@typeassert(y=list)  # 只鉴定部分参数
def g(x, y):
    print(x, y)


print('按设定类型调用f:')
f('abc', 2, [1, 2, 3])
print('按错误类型调用f：')
f('abc', 2, 3)

'''
课后小结&拓展：
    1.带参数的装饰器，其原型是一个三层嵌套的高阶函数。第一次调用返回装饰器函数（带参数），再调用则返回内置函数
    一般结构是:
    def typeassert(*ty_args, **ty_kwargs):  # 按实际用途取名
        def decorator(func):
               def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
    2.signature.bind(self, args, kwargs, *, partial=False):
    inspect 下的signaure(func)，可以返回函数对象的参数信息。
    旗下的bind方法，可以创建一个“参数：参数值”的字典，args和kwargs就是自己设定的参数值，数量必须与参数个数一致
    而bind_partical方法则可以实现只赋值部分参数
    bind.arguments 方法可以返回上述映射关系的有序字典。
'''