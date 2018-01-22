#!usr/bin/python3
# -*- coding: UTF-8 -*-

# lesson6-4---如何创建xml文档

# 案例：把平安股票csv文件，转换成相应的xml文件

# 方案：使用标准库中的xml.etree.ElementTree,构建ElementTree,使用writer方法写入文件

# 利用下载过来的csv，创建一个第一行都是英文字母的副本pingan4.csv

import chardet
import csv


with open('pingan3.csv', 'rb') as p3:
    f_coding = chardet.detect(p3.read())
    print('原始文本的编码是：', f_coding['encoding'])

with open('pingan3.csv', 'r', encoding=f_coding['encoding'], newline='') as p3:
    reader = csv.reader(p3)
    print('原始文本的头部信息是：', next(reader))
    header = ['Date', 'Code', 'Name', 'Close', 'High', 'Low', 'Open', 'Volume']
    print('副本的头部信息是：', header)
    with open('pingan4.csv', 'w') as p4:
        writer = csv.writer(p4)
        writer.writerow(header)
        for row in reader:
            writer.writerow(row)

# 构建xml文件
from xml.etree.ElementTree import Element, ElementTree


with open('pingan4.csv', 'r', newline='') as p4:
    reader = csv.reader(p4)
    header = next(reader)

    root = Element('Data')
    for row in reader:
        e1 = Element('Row')
        i = 0
        for tag in header:
            e2 = Element(tag)
            e2.text = row[i]
            e1.append(e2)
            i += 1
        root.append(e1)

rt = ElementTree(root)
rt.write('demo.xml')
print('end')

# 课后小结&拓展：
#     1.构建xml文件，使用 Element 创建节点，使用Element.append()方法连接父子节点，使用Element.text为节点增加文本信息
#     使用ElementTree创建节点树。使用ElementTree.write创建xml文件