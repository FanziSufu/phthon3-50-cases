#!usr/bin/python3
# -*- coding: UTF-8 -*-

# lesson5-4---如何将文件映射到内存

# 案例（应用）：1.在访问某些二进制文件时，希望能把文件映射到内存中，可以实现随机访问（framebuffer设备文件）
# 2.某些嵌入式设备，寄存器被编址到内存地址空间，我们可以映射/dev/mem某范围，去访问这些寄存器
# 3.如果多个进程映射同一个文件，还能实现进程通信的目的

# 方案：使用标准库中mmap模块的mmap()函数，它需要一个打开的文件描述符作为参数

import mmap


f = open('demo.bin', 'r+b')
m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)  # 建立demo.bin的内存映射，权限为读写，大小为demo.bin的大小
print('修改前的m[:1]', m[:1])  # 在python3中 打印m[0]会返回整数，而打印序列的形式，可以返回二进制数据
m[:1] = b'\x88'
print('修改后的m[:1]', m[:1])
print('修改前的m[4:8]', m[4:8])
m[4:8] = b'\xaa' * 4  # 注意字节数要一致
print('修改后的m[4:8]', m[4:8])
m.close()

# 将demo.bin的一部分映射到内存中

m = mmap.mmap(f.fileno(), mmap.PAGESIZE * 3, access=mmap.ACCESS_WRITE, offset=mmap.PAGESIZE * 2)  # 将demo.bin,从第2 * mmap.PAGESIZE位置起
# 的mmao.PAGESIZE * 3 个字节的内容，映射到内存中

# 再做上述一样的修改，可以发现不是覆盖，而是在新的位置做了修改

print('修改前的m[:1]', m[:1])
m[:1] = b'\x88'
print('修改后的m[:1]', m[:1])
print('修改前的m[4:8]', m[4:8])
m[4:8] = b'\xaa' * 4
print('修改后的m[4:8]', m[4:8])
m.close()
f.close()

# 课后小结&拓展
#     1.mmap.mmap(fileno, length, flags=MAP_SHARED, prot=PROT_WRITE|PROT_READ, access=ACCESS_DEFAULT[, offset])（UNIX系统）
#     mmap是一种虚拟内存映射文件的方法，即讲一个文件或者其他对象映射到进程的地址空间，实现文件磁盘地址和进程虚拟地址空间中
#     一段虚拟地址的一一对映关系。
#     fileno：文件描述符，可以用file.fileno()获得也可以由os.open获得。
#     length：要映射文件部分的大小（以字节为单位），为0.则映射整个文件，如果length大于文件当前大小，则扩展这个文件
#     flags:两个值。MAP_PRIVATE,表示只有本进程可用；MAP_SHARED表示将内存映射与其他进程共享，是默认值。
#     prot:mmap.PROT_READ, mmap.PROT_WRITE 和 mmap.PROT_WRITE | mmap.PROT_READ。最后一者的含义是同时可读可写，默认值。
#     access:ACCESS_READ:只读访问   ACCESS_WRITE:读写访问，默认 ACCESS_COPY:拷贝访问，不会把更改写入到文件，使用flush把更改写到文件。
