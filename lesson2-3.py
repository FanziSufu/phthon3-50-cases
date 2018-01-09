# !usr/bin/python3
# -*- coding: UTF-8 -*-

# lesson2-3---如何统计序列中元素出现频度

# 案例1：从某随机序列中，找出出现次数最高的3个元素，他们出现的次数是多少

# 方案一：自定义一个函数求解


from random import randint

data = [randint(0, 9) for _ in range(20)]
print(data)


def count(l, num=3):
    d = dict.fromkeys(l, 0)
    for x in l:
        d[x] += 1
    l2 = sorted(list(d.items()), key=lambda i: i[1], reverse=True)
    return dict(l2[0:num])


print(count(data, 3))


# 方案二：使用collections.Counter对象，将序列传入Counter的构造器，得到Counter对象是元素频度的字典。
# 使用Counter.most_common(n)方法可以得到频度最高的n个元素的列表。

from collections import Counter

c = Counter(data)
print(c.most_common(3))

# 案例2：对某英文文章的单词，进行词频统计，找出次数最高的10个单词，并给出初选的次数

import re

txt = r'''Wherever you are,and whoever you may be, there is one thing in 
which you and I are just alike, at this moment, and in all the 
moments of our existence. We are not at rest; we are on a journey. 
Our life is not a mere fact; it is a movement, a tendency, a steady, 
ceaseless progress towards an unseen goal. We are gaining 
something, or losing something, every day. Even when our position 
and our character seem to remain precisely the same, they are 
changing. For the mere advance of time is a change. It is not the 
same thing to have a bare field in January and in July. The season 
makes the difference. The limitations that are childlike in the child 
are childish in the man.
Everything that we do is a step in one direction or another. Even the 
failure to do something is in itself a deed. It sets us forward or 
backward. The action of the negative pole of a magnetic needle is 
just as real as the action of the positive pole. To decline is to accept 
the other alternative.
Are you richer today than you were yesterday? No? Then you are a 
little poorer. Are you better today than you were yesterday? No? 
Then you are a little worse. Are you nearer to your port today than 
you were yesterday? Yes, you must be a little nearer to some port 
or other; for since your ship was first launched upon the sea of life 
you have never been still for a single moment; the sea is too deep, 
you could not find an anchorage if you would; there can be no 
pause until you come into port.'''

c2 = Counter(re.split('\W+', txt))  # 按非字母分割并返回给Counter()
print(c2.most_common(10))
