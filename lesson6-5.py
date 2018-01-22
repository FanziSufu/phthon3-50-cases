#!usr/bin/python3
# -*- coding: UTF-8 -*-

# lesson6-5---如何读写excel文件

# 案例：Microsoft Excel 是日常办公中使用最频繁的软件，其格式为xls，xlsx，一种非常常用的电子表格
# 某班成绩，记录在excel文件demo.xlsx中：
# 姓名  语文  数学  外语
# 李雷   95   99   96
# 韩梅   98   100  96
# 张峰   94   95   95
# 利用python读写excel，添加“总分”列，计算每人总分。

# 方案：使用第三方库xlrd和xlwt，这两个库分别用于excel读和写

import xlrd
import xlwt


# 读取demo.xlsx文件
book = xlrd.open_workbook('demo.xlsx')
sheet = book.sheet_by_index(0)

sheet.put_cell(0, 4, 1, '总分', None)  # 1 是数据类型，表示 字符型， None 是数据格式（对齐方式等）
for r in range(1, sheet.nrows):
    value = sum(sheet.row_values(r, 1, None))
    sheet.put_cell(r, 4, 2, value, None)  # 2 是数据类型，表示 数字型

# 创建读文件的副本output.xlsx
wbook = xlwt.Workbook()
wsheet = wbook.add_sheet(sheet.name)
style = xlwt.easyxf('align: vertical center, horizontal center')

for r in range(sheet.nrows):
    for c in range(sheet.ncols):
        wsheet.write(r, c, sheet.cell(r, c).value, style)

wbook.save('output.xlsx')

# 课后小结&拓展：
#     1.xlrd只能读取excel文件，而不能对原文件进行修改。
#     2.利用xlwt写文件，最后要用save保存好。
