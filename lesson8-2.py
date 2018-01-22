#!usr/bin/python3
# -*- coding: UTF-8 -*-

'''
lesson8-2---如何线程间通信

案例：从新浪财经下载多只股票的csv数据，并将其转换为xml文件。由于全局解释器锁的存在，多线程进行cpu密集型操作不能
提高执行效率，我们修改程序构架：
1.使用多个DownloadThread线程进行下载（I/O）操作
2.使用一个ConvertThread线程进行转换（CPU密集型操作）
3.下载线程把下载数据安全地传递给转换线程

方案：使用标准库中Queue.Queue，它是一个线程安全的队列。
Download线程把下载数据放入队列，Convert线程从队列里提取数据。
'''

import requests
from io import StringIO
from xml.etree.ElementTree import Element, ElementTree
from queue import Queue
from threading import Thread
import csv


# 创建下载线程
class DownloadThread(Thread):
    def __init__(self, sid, queue):
        Thread.__init__(self)
        self.sid = sid
        self.queue = queue
        self.url = 'http://quotes.money.163.com/service/chddata.html?\
            code=1%s&start=20100102&end=20180118\&fields=TCLOSE;HIGH;LOW;TOPEN;VATURNOVE'
        self.url %= str(self.sid).rjust(6, '0')

    def download(self):
        response = requests.get(self.url, timeout=3)
        if response.ok:
            return StringIO(response.content.decode('GB2312'))

    def run(self):
        print('Download...%d' % self.sid)
        data = self.download()
        self.queue.put((self.sid, data))


# 创建转换线程
class ConvertThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def csvToXml(self, scsv, fxml):
        reader = csv.reader(scsv)
        next(reader)
        headers = ['Date', 'Code', 'Name', 'Close', 'High', 'Low', 'Open', 'Volume']

        root = Element('Data')
        for row in reader:
            eRow = Element('Row')
            root.append(eRow)
            for tag, text in zip(headers, row):
                e = Element(tag)
                e.text = text
                eRow.append(e)

        et = ElementTree(root)
        et.write(fxml)

    def run(self):
        while True:
            sid, data = self.queue.get()
            print('Convert...%d' % sid)
            if sid == -1:  # 设置跳出循环的入口
                break
            if data:  # 如果碰到股票代码对应的股票没有数据，则自动跳过
                fname = str(sid).rjust(6, '0')
                with open(fname + '.xml', 'wb') as wf:
                    self.csvToXml(data, wf)


# 开始主流程
if __name__ == '__main__':

    q = Queue()
    dThread = [DownloadThread(i, q) for i in  range(1, 11)]
    for t in dThread:
        t.start()
    cThread = ConvertThread(q)
    cThread.start()

    for t in dThread:
        t.join()

    q.put((-1, None))  # 手动设置参数，使所有子线程结束后，跳出转换循环

'''    
课后小结&拓展：
    1.本结的程序架构与上一节相比，把CPU密集型的convert操作从多线程中剥离出来，作为单线程执行。
    这种针对python不善于处理CPU密集型程序的特性的方法，使更多的资源用于处理多线程的IO操作，从而提高了效率
    2.本结内容，为了实现线程中的通信，使用了线程安全模块queue下的Queue()
    这个函数可以创建一个用于线程安全通信的栈，遵循先进先出的原则，利用put()和get()方法，实现线程间的通信
'''
