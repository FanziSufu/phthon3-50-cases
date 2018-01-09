# !usr/bin/python3
# -*- coding:UTF-8 -*-

# lesson3-4---如何进行反向迭代以及如何实现反向迭代？

# 案例：实现一个连续浮点数发生器FloatRange（和range类似），根据给定范围（start，end）
# 和步进值（step）产生一系列连续浮点数，如迭代FloatRange（1.0,3.0,0.5）可产生：
# 正向1.0  1.5  2.0  2.5  3.0
# 反向3.0  2.5  2.0  1.5  1.0
# 注意：本案例不考虑浮点数运算精度问题！


class FloatRange:
    def __init__(self, start, end, setp):
        self.start = start
        self.end = end
        self.step = setp

    def __iter__(self):
        number = self.start
        while number <= self.end:
            yield number
            number += self.step

    def __reversed__(self):
        number = self.end
        while number >= self.start:
            yield number
            number -= self.step


for x in FloatRange(1.0, 3.0, 0.5):
    print(x)

print('-' * 30)

for x in reversed(FloatRange(1.0, 3.0, 0.5)):
    print(x)

# 课后小结&拓展：
#     1.创建正序的可迭代对象类，需要包含__iter__方法，创建倒序的可迭代对象类，需要包含__reversed__方法
