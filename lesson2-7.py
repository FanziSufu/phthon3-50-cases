# !usr/bin/python3
# -*- coding:UTF-8 -*-

# lesson2-7---如何实现用户的历史记录功能（最多n条）

# 案例：制作一个简单的猜数字游戏，添加历史记录功能，显示用户最近猜过的数字，并具有保存、重载的功能

# 方法：使用collections中的deque实现历史记录功能，使用pickle的dump和load实现保存和重载的功能

from random import randint
from collections import deque
import pickle


N = randint(0, 100)
history = deque([], 5)


def guess(n):
    if n == N:
        print('恭喜你，猜对了！')
        return True
    elif n < N:
        print('您猜的数字小了，输入再大点的数字试试？！')
    else:
        print('您猜的数字大了，输入再小点的数字试试？！')


while True:
    line = input('请输入一个数字：')
    if line.isdigit():
        k = int(line)
        history.append(k)
        if guess(k):
            break
    elif line == 'history' or line == 'h?':
        print(list(history))
    elif line == 'save':
        with open('history', 'wb') as f:
            pickle.dump(history, f)
        with open('res', 'wb') as f:
            pickle.dump(N, f)
        print('保存成功！')
    elif line == 'load':
        with open('history', 'rb') as f:
            history = pickle.load(f)
        with open('res', 'rb') as f:
            N = pickle.load(f)
        print('载入成功')
    else:
        print('指令错误！')
