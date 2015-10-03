# -*- coding:utf-8-*-
# 一些配置信息和公共类
import datetime
import time

dim_items_file = '../source_data/dim_items.txt'
dim_fashion_matchsets_file = '../source_data/dim_fashion_matchsets.txt'
test_items_file = '../source_data/test_items.txt'
res_test_items_file = '../data/fm_submissions.txt'

log_file = '../log/log.txt'
log_file_fd = open(log_file, 'w')

def write_log(lineno, msg):
     print >> log_file_fd, "%s\t[%s]\tlog_msg: %s" % (datetime.datetime.now(), str(lineno), msg)
     log_file_fd.flush()

def write_log(msg):
    print >> log_file_fd, "%s\tlog_msg: %s" % (datetime.datetime.now(), msg)
    log_file_fd.flush()

class Timer :
    def __init__(self):
	self.t = time.time()

    def get_diff(self):
	tmp = time.time()
	diff = tmp - self.t
	self.t = tmp
	return diff

