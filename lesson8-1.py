#!usr/bin/python3
# -*- coding: UTF-8 -*-

'''
lesson8-1---如何使用多线程

案例：从新浪财经下载多只中国深圳股市的csv数据文件，并将其转换成xml文件。
如何使用线程来提高下载和处理的速度？

方案：使用标准库threading.Thread创建线程，在每一个线程中下载并转换一只股票数据
'''

import requests
from io import StringIO
import csv
from xml.etree.ElementTree import Element, ElementTree
from threading import Thread


def download(url):
    response = requests.get(url, timeout=3)
    if response.ok:  # 响应成功
        return StringIO(response.content.decode('GB2312'))  # 先对下载的内容解码，再保存到缓存中


def csvtoXml(scsv, fxml):
    # 设置首行
    reader = csv.reader(scsv)
    next(reader)  # 下载过来的文件，第一行解码后是中文，先pass掉
    headers = ['Date', 'Code', 'Name', 'Close', 'High', 'Low', 'Open', 'Volume']  # 手动翻译成英文，用作xml的节点

    # 转化节点
    root = Element('Data')
    for row in reader:
        eRow = Element('Row')
        root.append(eRow)
        for tag, text in zip(headers, row):
            e = Element(tag)
            e.text = text
            eRow.append(e)

    # 生成数并写入xml文件
    et = ElementTree(root)
    et.write(fxml)


class MyThread(Thread):
    def __init__(self, sid):
        Thread.__init__(self)
        self.sid = sid

    def run(self):
        self.handle()

    def handle(self):
        print('Downloading...(%d)' % self.sid)
        scode = str(self.sid).rjust(6, '0')  # 将传入参数转化为6位股票代码
        url = 'http://quotes.money.163.com/service/chddata.html?\
               code=1%s&start=20100102&end=20180118\&fields=TCLOSE;HIGH;LOW;TOPEN;VATURNOVER' % scode
        rf = download(url)
        if rf is None:
            return

        print('Convert to Xml...%d' % self.sid)
        with open(scode + '.xml', 'wb') as wf:
            csvtoXml(rf, wf)


threads = []
for i in range(1, 11):
    t = MyThread(i)
    threads.append(t)
    t.start()

for t in threads:
    t.join()  # 使所有线程结束后再退出主线程

print('main thread')

'''
课后小结&拓展：
    1.requests.get().ok用于判断是否成功访问服务器，访问成功则返回Ture
    2.io.StringIO()用于缓存下载过来的文本内容。注意对下载内容进行解码
    3.threading.Thread(group=NOne,target=None,name=None,args=(),kwargs={},*,daemon=None)
    创建线程。一般使用的参数是target,args,(kwargs),target是run()调用的函数,后两者是target的参数
    注意：调用该方法时，设置参数要使用关键字参数的方式
    4.Thread.start() 表示线程开始，Thread.join()是阻塞函数，用于保证线程在主线程之前结束。
    5.python其实一次只能执行一个线程，由一个全局锁GIL控制。通过快速切换线程，使之从结果上到底多线程的效果。
    也正因为如此，python善于处理IO密集型的程序（如本例中下载csv），而不善于处理cpu密集型的程序（如本例中转换成xml）。
'''