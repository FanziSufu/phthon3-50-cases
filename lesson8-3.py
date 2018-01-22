#!usr/bin/python3
# -*- coding: UTF-8 -*-

'''
lesson8-3---如何在线程间进行事件通知

案例：对于上一结的程序，现在增加额外需求：
实现一个线程，将转换出的xml文件压缩打包，比如转换线程每生产出5个xml文件，就通知打包线程将它们打包成一个xxx.tgz文件
并删除xml文件。打包完成后，打包线程反过来通知转换线程，转换线程继续转换

方案：线程间的事件通知，可以使用标准库中Thread.Event：
1.等待事件一端调用wait，等待事件
2.通知事件一端调用set，通知事件
'''

import requests
from io import StringIO
from xml.etree.ElementTree import Element, ElementTree
from queue import Queue
from threading import Thread, Event
import csv
import os
import tarfile


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
    def __init__(self, queue, cEvent, tEvent):
        Thread.__init__(self)
        self.queue = queue
        self.cEvent = cEvent
        self.tEvent = tEvent

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
        count = 0
        while True:
            sid, data = self.queue.get()
            print('Convert...%d' % sid)
            if sid == -1:  # 设置跳出循环的入口
                self.cEvent.set()
                self.tEvent.wait()
                break
            if data:  # 如果碰到股票代码对应的股票没有数据，则自动跳过
                fname = str(sid).rjust(6, '0')
                with open(fname + '.xml', 'wb') as wf:
                    self.csvToXml(data, wf)
                count += 1
            if count == 5:
                self.cEvent.set()
                self.tEvent.wait()
                self.tEvent.clear()
                count = 0


# 创建打包线程
class TarThread(Thread):
    def __init__(self, cEvent, tEvent):
        Thread.__init__(self)
        self.count = 0
        self.cEvent = cEvent
        self.tEvent = tEvent
        self.setDaemon(True)  # 设置打包线程为守护线程，主线程结束后自行销毁，而无需再补充run()中跳出循环的代码

    def tarxml(self):
        self.count += 1
        tarname = '%d.tgz' % self.count
        tar = tarfile.open(tarname, 'w:gz')  # 创建压缩包，写入模式，gz格式
        for fname in os.listdir('.'):  # 遍历文件所在目录文件
            if fname.endswith('.xml'):  # 查找xml文件
                tar.add(fname)  # 打包xml文件
                os.remove(fname)  # 删除xml文件
        tar.close()

        if not tar.members:  # 如果不存在xml文件
            os.remove(tar)  # 则删除压缩包

    def run(self):
        while True:
            self.cEvent.wait()  # 进入等待状态，等待转换线程发来启动（set）指令
            self.tarxml()  # 收到set指令后，开始执行打包操作
            self.tEvent.set()  # 打包完成，发回set指令给转换线程，使继续执行转换操作

            self.cEvent.clear()  # 恢复wait，使可以再次执行等待操作


# 开始主流程
if __name__ == '__main__':

    q = Queue()
    cEvent = Event()
    tEvent = Event()
    dThread = [DownloadThread(i, q) for i in range(1, 17)]
    cThread = ConvertThread(q, cEvent, tEvent)
    cThread.start()
    tThread = TarThread(cEvent, tEvent)
    tThread.start()

    for t in dThread:
        t.start()

    for t in dThread:
        t.join()

    q.put((-1, None))  # 手动设置参数，使所有子线程结束后，跳出转换循环

'''
课后小结&拓展：
    1.Event()
    当执行线程时，如果遇到Event.wait()，线程就会进入等待状态，如果在接收到Event.set()指令，则进入执行接待
    值得注意的是，wait()是一次性的，如果要重复使用，需要使用Event.clear()指令，恢复wait()的活力
    2.setDaemon(True)
    本例中，线程cThread启动了线程tThread，会调用tThread.setDaemon，如果值为true，则将其视为守护线程，那么
    线程cThread结束时，也会将该守护线程杀死。所以当cThread跳出循环而结束线程时，tThread也自动结束，而无需
    再为其补充跳出死循环的语句
'''