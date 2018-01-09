# !usr/bin/python3
# -*- coding:UTF-8 -*-

# lesson5-8---如何处理二进制文件

# 案例：wav是一种音频文件的格式，音频文件为二进制文件。wav文件由头部信息和音频采样数据构成。前44个字节为头部信息，
# 包括声道数，采样频率，PCM位宽等等，后面是音频采样数据。使用python，分析一个wav文件头部信息；处理音频数据

# 方案：用struct.unpack方法分析头部信息；用二进制文件的读写，处理音频数据.

# 分析头部信息：

import struct


f = open('demo.wav', 'rb')

info = f.read(44)
print('头部信息的原始文本是：\n', info)

print('Num Chanels:', struct.unpack('h', info[22:24]))
print('ByteRate', struct.unpack('i', info[28:32]))
print('BlockAlign', struct.unpack('h', info[32:34]))

# 处理音频数据
print('-' * 30, '开始处理音频数据', '-' * 30)

import array


f.seek(0, 2)
n = (f.tell() - 44) // 2
buf = array.array('h', [])
f.seek(44)
buf.fromfile(f, n)
for i in range(n):
    buf[i] //= 8

f2 = open('demo2.wav', 'wb')
f2.write(info)
buf.tofile(f2)
f.close()
f2.close()
print('音频处理成功！请播放demo2.wav,看看声音是不是小了！？')

# 课后小结&拓展
#     1.struct.unpack(fmt, buffer)
#     位于struct模块，作用是把待解析字符串buffer，解析成fmt格式。
#     例如struct.unpack('h', '/x01/x02')，'h'指的是 short 型的整型，占2个字节，它要求待解析的字符串也占2个字节
#     '/x01/x02'是十六进制的字符串，按照'h'格式，（按小端字符序）解析后，是2*256^1+1*256^0=513
#     如果是按照大端字符序解析，则fmt为'>h'，那么解析结果是1*256^1+2*256^0=258
#     由此可见，小端字符序是从地位到高位读取，而大端字符序是从高位到地位读取（跟我们人类的习惯一致）
#     对计算机计算而言，小端字符序的计算速度更快。
#     2.fileObject.seek(offset[, whence])
#     用于移动文件读取指针到指定位置。offset表示需要偏移的字节数
#     whence默认为0，表示从文件开头开始算起，若为1，则表示从当前位置开始算起，若为2则表示从末尾算起
#     所以f.(0, 2)表示将指针移至文末. 再利用f.tell()，就可以得到文件的字节数
#     3.array.array(typecode,[, initializer])
#     用来创建数据类型相同的数组。
#     typecode表示数据类型，可以直接使用struct模块中的fmt。initializer表示初始值。这个值可以是列表，类字节对象，
#     可迭代对象，迭代器等
#     4.array.fromfile(f, n)
#     从文件f中，当前指针位置起，依次选取n个字符或字节，添加到数组array.array末端
#     5.因为python3中readinto被废除，所以语句处理做了一点修改。测试OK