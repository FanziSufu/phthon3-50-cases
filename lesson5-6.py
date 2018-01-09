#!usr/bin/python3
# -*- coding: UTF-8 -*-

# lesson5-6如何使用临时文件

# 案例：某项目中，我们从传感器采集数据，每收集到1G数据后，做数据分析，最终只保存分析结果。这样很大的临时数据如果常驻内存，
# 将消耗大量内存资源，我们可以使用临时文件存储这些临时数据（外部存储）。临时文件不用命名，且关闭后会自动被删除

# 方案：使用标准库中tempfile下的TemporaryFile,NamedTemporaryFile

import tempfile
import os


f = tempfile.TemporaryFile()  # 创建一个全部使用默认参数的临时文件
f.write(b'good job!')  # 默认创建二进制文件
f.seek(0)  # 使指针回到开头
print('读取写入文本：', f.read())  # 读取写入文本
f.close()  # 关闭后自动删除文本文件

print('-' * 30, '以下测试NamedTemporaryFile', '-' * 30)

f2 = tempfile.NamedTemporaryFile(mode='w+', delete=False)  # 创建一个文本格式，且关闭后不删除的临时文件
print('临时文件的文件名是：', f2.name)
f2.write('hello python!')
f2.seek(0)
print('读取写入文本：', f2.read())
f2.close()
print(r'临时文件f2是否在/tmp目录下：', f2.name[5:] in os.listdir('/tmp'))

# 课后小结&拓展:
#     1.tempfile
#     创建临时文件和临时目录的模块。与mkstemp(),mkdtemp()相比，tempfile创建的文件会在关闭后自动删除，而后者需要手动
#     2.tempfile.TemporaryFile(mode='w+b', buffering=None, encoding=None, newline=None, suffix=None, prefix=None,dir=None)
#     参数很多，重点关注mode，buffering。跟open()的参数有点像。但临时文件允许mode='w+t', buffering=None 这种情况
#     3.tempfile.NamedTemporaryFile(mode='w+b', buffering=None, encoding=None, newline=None, suffix=None, prefix=None,dir=None, delete=True)
#     比tempfile.TemporaryFile多了一个delete参数，如果Ture，则关闭后删除文件，如为False，则保留文件。可通过tempfile.NamedTemporaryFile.name，查看路径和文件名
