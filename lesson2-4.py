# !usr/bin/python3
# -*- coding:UTF-8 -*-

# lesson2-4---如何根据字典中值的大小，对字典中的项排序

# 案例：对记录学生姓名和分数的字典，返回按分数排序的列表

# 方案一：使用zip函数

from random import randint

student_score = {x: randint(60, 100) for x in 'xyzabc'}

print(student_score)
print(sorted(zip(student_score.values(), student_score.keys())))

# 方案二：利用sorted函数的key

print(sorted(list(student_score.items()), key=lambda x: x[1]))
