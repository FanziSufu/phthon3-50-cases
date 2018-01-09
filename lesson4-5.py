# !usr/bin/python3
# -*- coding:UTF-8 -*-

# lesson4-5---如何对字符串进行左，中，右对齐？
#
# 案例：对字典 {'lodDist': 100.0, 'SmallCull': 0.04, 'DistCull': 500.0, 'trilinear': 40, 'farclip': 477}
# 的迭代结果，打印使左对齐
#
# 方案一：使用字符串的str.ljust(),str.rjust(),str.center()进行左、右、中对齐

d = {'lodDist': 100.0, 'SmallCull': 0.04, 'DistCull': 500.0, 'trilinear': 40, 'farclip': 477}
w = max(map(len, d.keys()))  #求键值的最大字符数
for k in d:
    print(k.ljust(w), ':', d[k])

# 方案二：使用format()方法，传递类似'<20','>20','^20'的参数完成同样的任务
print('-' * 30, '以下是方案二的结果', '-' * 30)
for x in d:
    print(format(x, '<%s' % w), ':', d[x])  #如果不用占位符，会报错

# 课后小结&拓展：
#     1.str.ljust(width[, fillchar])
#     字符串方法，设定长度width（正整数），用fillchar字符串，往右填充剩余长度，右对齐，居中对齐同理
#     2.format（value[, format_spec]
#     这是内建函数，有别于str.format(),format_spec的用法相对复杂，涉及对齐的有'<'，'>'，'^'，'=',详见官方文档