#!usr/bin/python3
# -*- coding: UTF-8 -*-

"""
lesson7-3---如何让对象支持上下文管理

案例：我们实现了一个telnet客户端的类TelnetClient，调用实例的start()方法启动客户端与服务器交互，
交互完毕后需调用cleanup()方法，关闭已连接的socket，以及将操纵历史记录写入文件并关闭。
能否让TelnetClient的实例支持上下文管理协议，从而替代手工调用cleanup()方法

方案：实现上下文管理协议，需定义实例的__enter__,__exit__方法，它们分别在with开始和结束时被调用.
"""


from telnetlib import Telnet
from sys import stdout, stdin
from collections import deque

''' 不支持上下文管理协议的写法
class TelnetClient(object):
    def __init__(self, addr, port=23):
        self.addr = addr
        self.port = port
        self.tn = None

    def start(self):
        self.tn = Telnet(self.addr, self.port)
        self.history = deque()

        # user
        t = self.tn.read_until(b'login: ')
        stdout.write(t.decode('utf-8'))
        user = stdin.readline()
        self.tn.write(user.encode('utf-8'))

        # password
        t = self.tn.read_until(b'Password: ')
        if t.decode('utf-8').startswith(user[: -1]):
            t = t[len(user) + 1:]
        stdout.write(t.decode('utf-8'))
        print('')
        self.tn.write(stdin.readline().encode('utf-8'))

        # 与服务器交互
        t = self.tn.read_until(b'$ ')
        stdout.write(t.decode('utf-8'))
        while True:
            unique = stdin.readline()
            if not unique:
                break
            self.tn.write(unique.encode('utf-8'))
            self.history.append(unique)
            t = self.tn.read_until(b'$ ')
            stdout.write(t[len(unique) + 1:].decode('utf-8'))

    def cleanup(self):
        self.tn.close()
        self.tn = None
        with open(self.addr + '_history.txt', 'w') as f:
            f.writelines(self.history)


client = TelnetClient('127.0.0.1')
print('\nstart')
client.start()
print('\nend')
client.cleanup()
'''

# 支持上下文管理协议的写法


class TelnetClient(object):
    def __init__(self, addr, port=23):
        self.addr = addr
        self.port = port
        self.tn = None
        self.history = None

    def __enter__(self):
        self.tn = Telnet(self.addr, self.port)
        self.history = deque()
        return self

    def start(self):
        # user
        t = self.tn.read_until(b'login: ')
        stdout.write(t.decode('utf-8'))
        user = stdin.readline()
        self.tn.write(user.encode('utf-8'))

        # password
        t = self.tn.read_until(b'Password: ')
        if t.decode('utf-8').startswith(user[:-1]):  # 这条语句若注释掉，对结果没有影响，但若删除，则会打印出不明字符
            t = t[len(user) + 1:]
        stdout.write(t.decode('utf-8'))
        print('')
        self.tn.write(stdin.readline().encode('utf-8'))

        # 与服务器交互
        t = self.tn.read_until(b'$ ')
        stdout.write(t.decode('utf-8'))
        while True:
            unique = stdin.readline()
            if not unique:
                break
            self.tn.write(unique.encode('utf-8'))
            self.history.append(unique)
            t = self.tn.read_until(b'$ ')
            stdout.write(t[len(unique) + 1:].decode('utf-8'))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tn.close()
        self.tn = None
        with open(self.addr + '_history.txt', 'w') as f:
            f.writelines(self.history)


with TelnetClient('127.0.0.1') as client:
    client.start()

'''
课后小结&拓展：
    1.telnet，是远程访问服务器的协议。利用telnetlib模块，可以实现从客户端访问服务器，并进行交互
    2.telnetlib.Telnet()，传入地址参数和端口参数，可以建立到服务器的连接
    3.Telnet.read_until()，在python中，需要传入字节类型的参数，所以本例中都加了'b'，
    4.Telnet.write()在写入时，也要对数据进行编码，并且要以'\n'结尾。
    5.stdout 与 stdin
    简单地说，stdout.write() 的功能与 print()相似，执行时，后者会多打印一个'\n'
    stdin.readline() 的功能与 input()相似，执行时，前者会多返回一个'\n'
    6.要让类对象具有上下文功能，需要定义__enter__和__exit__
    ①with语句在开始调用类时，先执行__enter__。__enter__需要返回值，通常是自身self
    ②with语句在结束调用类时，无论是否发生异常，都会执行__exit__函数的内容。__exit__有3个跟异常相关的参数。
'''
