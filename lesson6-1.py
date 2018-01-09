#!usr/bin/python3
# -*- coding: UTF-8 -*-

# lesson6-1---如何读写csv数据？

# 案例：http://quotes.money.163.com/service/chddata.html?code=0601318&start=20161201&end=20171231&fields=TCLOSE;HIGH;LOW;TOPEN;VOTURNOVER;VATURNOVER;TCAP;MCAP
# 我们可以通过上面的链接，从网易财经获得中国股市（深市），平安银行2016年12月1日至2017年12月31日的交易数据，它以csv数据格式存储。
# 请下载该csv文件，确定其编码，并将2017年中成交量超过5000000的记录存储到另一个csv文件中

# 使用urllib.request模块下的urlretrieve下载文件，使用chardet模块下的detect确定其编码，使用csv模块的reader，writer完成读写

import urllib.request
import chardet
import csv


urllib.request.urlretrieve('http://quotes.money.163.com/service/chddata.html?'
            'code=0601318&start=20161201&end=20171231&fields=TCLOSE;HIGH;LOW;'
            'TOPEN;VOTURNOVER;VATURNOVER;TCAP;MCAP', 'pingan.csv')  # 下载csv文件

with open('pingan.csv', 'rb') as f:
    f_coding = chardet.detect(f.read())
    print('pingan.csv的编码是：', f_coding['encoding'])  # 获取 pingan.csv的编码

with open('pingan.csv', 'r', encoding=f_coding['encoding'], newline='') as rf:
    reader = csv.reader(rf)
    headers = next(reader)
    print('该文件的头部信息是：', headers)
    with open('pingan2.csv', 'w', encoding=f_coding['encoding'], newline='') as wf:
        writer = csv.writer(wf)
        writer.writerow(headers)
        for row in reader:
            if row[0] < '2017-01-01':
                break
            if float(row[8]) >= 50000000.0:
                writer.writerow(row)

with open('pingan2.csv', 'r', encoding=f_coding['encoding'], newline='') as wf:
    for row in wf:
        print(row)

# 课后小结&拓展：
#     1.urllib.request.urlretrieve(url, filename=None, reporthook=None,data=None)
#     在python3中，urlretrieve被放置urllib.request模块下。跟python2有点不同。
#     2.在python2中，我们对csv进行读写时，都是用二进制的形式，但到了python3，因为字符串的语义发生了变化，使用二进制读写可能导致无法打印的问题。
#     所以我们用文本的形式读写文件。这时，用open()打开文件时，要注意设置encoding的值，使其为csv文件的编码（python3默认utf-8编码，若文件不是
#     utf-8，会导致无法解析），使用chardet下的detect可以确定文件的编码。另外最好设置newline=‘’,防止出现多余空行的结果。
#     3.csv模块最常用的是reader，和writer方法，其用法在代码中已展示。