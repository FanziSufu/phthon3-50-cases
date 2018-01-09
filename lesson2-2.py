# !usr/bin/python3
# -*-coding:UTF-8 -*-

# lesson2-2---如何为元组中的每个元素命名，提高程序可读性？

# 案例：使用索引访问学生信息元组，提高程序可读性

# 方案一：定义类似于其他语言的枚举类型，也就是定义一系列数值常量

Student = ('Jim', 16, 'male', 'jim8721@gmail.com')
NAME, AGE, SEX, EMAIL = range(4)
print(Student[NAME])
print(Student[AGE])
print(Student[SEX])
print(Student[EMAIL])

# 方案二：使用标准库中collections.namedtuple替代内置tuple

from collections import namedtuple

Student = namedtuple('Student', ['name', 'age', 'sex'])
s = Student('goten', 25, 'mail')

print(s.name)
print(s.age)
print(s.sex)
print(isinstance(s, tuple))
