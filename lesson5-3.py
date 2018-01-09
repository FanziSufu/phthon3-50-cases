#!usr/bin/python3
# -*- coding: UTF-8 -*-

# lesson5-3---如何设置文件的缓冲

# 案例：将文件内容写入到硬件设备时，使用系统调用，这类I/O操作的时间很长，为了减少I/O操作的次数，文件通常使用缓冲区。
# （有足够多的数据才进行系统调用）文件的缓冲行为，分为全缓冲，行缓冲，无缓冲

# 方案：利用open函数的buffering参数

# 全缓冲，设置buffering为大于1的整数n,n为缓冲区大小;或者使用默认值-1或小于0的整数
f = open('test.txt', 'w')  # 经测试发现，本环境下，默认的缓冲区大小为8192，而同计算机在python2下为4096
f = open('test.txt', 'w', buffering=12288)
f = open('test.txt', 'w', buffering=2048)  # 经测试发现，当设置的buffering小于8192，如2048，当字节数大于2048而小于
# 8192时，数据仍在缓存区而未被写入文本。 在python2下测试。当数据大于2048而小于4096时，超出2048即能写入文本


# 行缓冲，设置open函数的buffering的值为1，出现换行符\n，就将缓冲区数据写入文本
f = open('test.txt', 'w', buffering=1)  # python3中，只有文本格式才能设置buffering=1

# 无缓冲，设置open函数的buffering的值为0，将程序内容直接写入文件
f = open('test.txt', 'wb', buffering=0)  # python3中，只有二进制格式的才能设置buffering=0
