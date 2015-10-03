# -*- coding:utf-8-*-
# 一些配置信息和公共类


dim_items_file = '../source_data/dim_items.txt'
dim_fashion_matchsets_file = '../source_data/dim_fashion_matchsets.txt'
test_items_file = '../source_data/test_items.txt'

err_log_file = '../log/err_log.txt'
err_log_file_fd = open(err_log_file, 'w')
def write_stderr(lineno, msg):
     print >> err_log_file_fd, "%s\t[%s]\terror_msg: %s" % (datetime.datetime.now(), str(lineno), msg)
