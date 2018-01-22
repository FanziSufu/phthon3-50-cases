#!usr/bin/python3
# -*- coding: UTF-8 -*-

# lesson6-3---如何解析简单的xml文档

# 案例：xml是一种十分常用的标记性语言，可提供统一的方法来描述应用程序的结构化数据：
# <?xml version="1.0"?>
# <data>
#     <country name="Liechtenstein">
#         <rank>1</rank>
#         <year>2008</year>
#         <gdppc>141100</gdppc>
#         <neighbor name="Austria" direction="E"/>
#         <neighbor name="Switzerland" direction="W"/>
#     </country>
# </data>
#
# python中如何解析xml文档？

# 方案：使用标准库中的xml.etree.ElementTree,其中的parse函数可以解析xml文档

from xml.etree.ElementTree import parse


# 获取demo.xml的根节点
tree = parse('demo.xml')
root = tree.getroot()

# 元素的属性
print('元素标签：', root.tag)
print('元素属性：', root.attrib)
print('元素文本：', root.text.strip())

for child in root:
    print('子元素的属性值：', child.get('name'))

print('find的用法，返回找到的第一个子元素：', root.find('country').get('name'))

for child in root.findall('country'):
    print('使用findall找出指定子元素的属性值：', child.get('name'))

# 功能与与findall一样，不同的是，使用iterfind生成的是生成器对象，更节省空间
for child in root.iterfind('country'):
    print('使用iterfind找出指定子元素的属性值：', child.get('name'))

print('使用iter找出所有的子元素：', list(root.iter()))
print('使用iter找出指定元素：', list(root.iter('rank')))

# 高级查找功能
print('查找孙子节点下的rank：', root.findall('*/rank'))
print('查找所有节点下的rank：', root.findall('.//rank'))
print('查找rank的父节点：', root.findall('.//rank/..'))
print('查找包含指定属性的子节点：', root.findall('country[@name]'))
print('查找包含指定属性值的子节点：', root.findall('country[@name="Singapore"]'))
print('查找包含指定标签的子节点：', root.findall('country[rank]'))
print('查找包含指定标签值的子节点：', root.findall('country[rank="68"]'))
print('查找指定位置的子节点：', root.findall('country[1]'))
