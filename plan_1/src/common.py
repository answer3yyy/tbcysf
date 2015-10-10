# -*- coding:utf-8-*-
# 一些配置信息和公共类
import datetime
import time

dim_items_file = '../source_data/dim_items.txt'
dim_fashion_matchsets_file = '../source_data/dim_fashion_matchsets.txt'
test_items_file = '../source_data/test_items.txt'
now_time = datetime.datetime.now()
now_time = now_time.strftime("%Y-%m-%d_%H_%M_%S")
res_test_items_file = '../data/fm_submissions.txt_%s' %(now_time)

log_file = '../log/log.txt'
log_file_fd = open(log_file, 'w')


dim_items_dump_file = '../data/dim_items_dump.txt'
cat_to_item_rindex_dump_file = '../data/cat_to_item_rindex_dump.txt'
cat_sim_rindex_dump_file = '../data/cat_sim_rindex_dump.txt'

word_iterm_base_dump_file = '../data/word_iterm_base_dump.txt'


train_data_output = '../data/train_data_output.txt'


class Item:
    def __init__(self):
	self.item_id = 0
	self.cat_id  = 0
	self.titles  = []
	self.pos     = 0

    def __init__(self, item_id, cat_id, titles, pos):
	self.item_id = item_id
	self.cat_id  = cat_id
	self.titles  = titles
	self.pos     = pos

    def __eq__(self, other):
	return \
	self.item_id == other.item_id and \
	self.cat_id  == other.cat_id  and \
	self.titles  == other.titles  and \
	self.pos     == other.pos





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

