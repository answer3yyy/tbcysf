# -*- coding:utf-8-*-
# 一些配置信息和公共类
import datetime
import time

dir = '../source_data/'
dir = '../test_data/'

dim_items_file = dir + 'dim_items.txt'
dim_fashion_matchsets_file = dir + 'dim_fashion_matchsets.txt'
test_items_file = dir + 'test_items.txt'
now_time = datetime.datetime.now()
now_time = now_time.strftime("%Y-%m-%d_%H_%M_%S")
res_test_items_file = '../data/fm_submissions.txt_%s' %(now_time)

log_file = '../log/log.txt'
log_file_fd = open(log_file, 'w')


dim_items_dump_file = '../data/dim_items_dump.txt'
cat_to_item_rindex_dump_file = '../data/cat_to_item_rindex_dump.txt'
cat_sim_rindex_dump_file = '../data/cat_sim_rindex_dump.txt'

word_iterm_base_dump_file = '../data/word_iterm_base_dump.txt'


sample_data_output = '../data/sample_data_output.txt'
test_data_output = '../data/test_data_output.txt'


test_feature_file = dir + 'test_feature.txt' 
pred_items_file   = dir + 'pred_items.txt'
pred_fm_res_file  = '../data/pred_fm_res.txt'



class Item:
    def __init__(self):
	self.item_id = 0
	self.cat_id  = 0
	self.titles  = []
	self.pos     = 0

    def __init__(self, item_id, cat_id, titles, pos=0):
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

    def hash_str(self):
	title_str = "_".join( map(str, self.titles) )
	return "%d_%d_%d_%s" % (self.item_id, self.cat_id, self.pos, title_str)






def write_log(lineno=-1, msg=''):
     print >> log_file_fd, "%s\t[%s]\tlog_msg: %s" % (datetime.datetime.now(), str(lineno), msg)
     log_file_fd.flush()


class Timer :
    def __init__(self):
	self.t = time.time()

    def get_diff(self):
	tmp = time.time()
	diff = tmp - self.t
	self.t = tmp
	return diff

