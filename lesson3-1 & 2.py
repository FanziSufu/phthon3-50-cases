# !usr/bin/python3
# -*- coding:UTF-8 -*-

# lesson3-1&2---如何实现可迭代对象和迭代器对象

# 案例：某软件要求，从网络抓取各个城市气温信息并依次显示：
# 北京：15~20
# 天津：17~22
# 长春：12~18
# ……
# 如果一次抓取所有城市天气再显示，显示第一个城市气温时，有很高的延时，并且浪费存储空间。我们期望以“用时访问”的策略，并且能把所有城市气温封装到
# 一个对象里，可用for语句进行迭代。如何解决？

# 方案:第一步：实现一个迭代器对象WeatherIterator，__next__方法，每次返回一个城市气温。
# 第二步：实现一个可迭代对象WeatherIterable，__iter__方法返回一个迭代器对象。

import requests
from collections import Iterator, Iterable


class WeatherIterator(Iterator):
    def __init__(self, cities):
        self.cities = cities
        self.index = 0

    def __next__(self):
        if self.index == len(self.cities):
            raise StopIteration
        city = self.cities[self.index]
        self.index += 1
        return self.getWeather(city)

    def getWeather(self, city):
        r = requests.get('http://wthrcdn.etouch.cn/weather_mini?city=' + city)
        data = r.json()['data']['forecast'][0]
        return '%s: %s, %s' % (city, data['low'], data['high'])


class WeatherIterable(Iterable):
    def __init__(self, cities):
        self.cities = cities

    def __iter__(self):
        return WeatherIterator(self.cities)


for x in WeatherIterator(['北京', '天津', '长春']):
    print(x)


print('-' * 40)
# 方案二：使用yield函数


class Weather:
    def __init__(self, cities):
        self.cities = cities

    def __iter__(self):
        for city in self.cities:
            yield self.getweather(city)

    def getweather(self, city):
        r = requests.get('http://wthrcdn.etouch.cn/weather_mini?city=' + city)
        data = r.json()['data']['forecast'][0]
        return '%s: %s, %s' % (city, data['low'], data['high'])


for x in Weather(['北京', '上海', '鄂尔多斯']):
    print(x)


# 课后小结&拓展：
#     1.collections模块中的Iterable和Iterator，是抽象基础类（ABC），用于程序的接口，不能直接使用，需要被继承。
#     2.requests是非常好用的网络工程库，各种网络请求都能简洁轻松实现
#     3.创建可迭代对象的时候，要配置__iter__，创建迭代器对象的时候，要配置__next__
