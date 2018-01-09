# !usr/bin/python3
# -*- codint:UTF-8 -*-

# lesson4-3---如何调整字符串中文本的格式?

# 案例：某软件的log文件，其中的日期格式为'yyyy-mm-dd':
# ......
# 2018-01-03 18:55:42 startup archives unpack
# 2018-01-03 18:55:42 install python-decorator:all <无> 4.0.6-1
# 2018-01-03 18:55:42 status half-installed python-decorator:all 4.0.6-1
# 2018-01-03 18:55:42 status unpacked python-decorator:all 4.0.6-1
# ......
#
# 我们想把其中日期改为美国日期的格式'mm/dd/yyyy'.
# '2018-01-03' => '01/03/2018',应该如何处理

# 方案：使用re.sub()方法，利用正则表达式的捕获组，补货每个部分内容，在替换字符串中调整各个捕获组的顺序

import re


f_name = open('/var/log/dpkg.log', 'r')
log = f_name.read()

print('-' * 30, '原始文本', '-' * 30)
print(log)

new_log = re.sub('(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})', r'\g<month>/\g<day>/\g<year>', log)

print('-' * 30, '替换后新文本', '-' * 30)
print(new_log)

f_name.close()

# 课后小结&拓展：
#     1.re.sub(pattern, repr, string, flags=0)
#     位于re模块，对于待替换的string,找到正则表达式pattern代表的内容，使用repr模式替换，repr可以使字符串，也可以是函数。
#     2.对于正则表达式,用‘（）’括起来，表示捕获组，?P<>可以给捕获组命名。捕获组的内容后期可以按需要引用