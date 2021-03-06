# -*- coding:utf-8 -*-

import sys
import common
from common import write_log
from common import Timer

class Strategy:
    def __init__(self):
	# 最后一共要返回多少个推荐结果
	self.total_rec_num = 200

	# 最多处理多少个sim_cat的商品
	self.max_sim_cat_process = 10


    def get_total_rec_num(self):
	return self.total_rec_num 

    def get_max_sim_cat_process(self):
	return self.max_sim_cat_process

    def num_to_return_of_this_sim_cat(self, sim_cat_idx):
	# sim_cat_idx 是这个sim_cat在所有相似性递减的sim_cat里面的下标值
	return self.total_rec_num






class Predictor :
    def __init__(self, 
		 dim_items_index_builder,    # item正排
	         cat_to_item_rindex_builder, # cat->item倒排
	         cat_sim_builder,            # cat之间的相似性
		 cat_sim_rindex_builder,     # cat->多个相似cat 的倒排
		 word_iterm_base_builder):   # 标题切词相关性
	self.dim_items_index    = dim_items_index_builder.get_res()
	self.cat_to_item_rindex = cat_to_item_rindex_builder.get_res()
	self.cat_sim            = cat_sim_builder.get_res()
	self.cat_sim_rindex     = cat_sim_rindex_builder.get_res()
	self.word_iterm_base    = word_iterm_base_builder.get_res()

	self.strategy = Strategy()
	pass

    def __cal_title_sim(self, title1, title2):
	total_val = 0.0
	for w1 in title1:
	    for w2 in title2:
		key = (w1, w2)
		val = self.word_iterm_base.get(key, 0)
		total_val += val
	return total_val


    def __find_sim_item_from_a_list(self, target_item, sim_item_ids, idx):
	target_title = target_item[1]
	
	count = 0
	rec_items = []
	for sim_id in sim_item_ids:
	    sim_item = self.dim_items_index.get(sim_id, -1)
	    if sim_item == -1 : continue

	    count += 1
	    if count > 20000: break

	    sim_title = sim_item[1]
	    timer = Timer()
	    val = self.__cal_title_sim(target_title, sim_title)
	    write_log(msg = "__cal_title_sim cost time:%f, target_title size:%d, sim_title size:%d" % (timer.get_diff(), len(target_title), len(sim_title)))
	    rec_items.append( (sim_id, val) )

	num_to_get = self.strategy.num_to_return_of_this_sim_cat(idx)
	if len(rec_items) > num_to_get:
	    rec_items.sort(lambda y,x : cmp(x[1], y[1]))
	    rec_items = rec_items[0: num_to_get]
	return rec_items

    
    def __get_rec_item_ids(self, item_id, sim_cat_ids):
	"""
	获取推荐item_id
	Args:
	    item_id: query的item_id
	    sim_cat_ids : item_id的相似cat_id列表
	Returns:
	    [(rec_item_id, sim_value), (rec_item_id, sim_value), ...],长度为strategy.get_total_rec_num()
	"""

	target_item = self.dim_items_index.get(item_id, -1)
	if target_item == -1:
	    write_log(sys._getframe().f_lineno, "cannot get info of item_id:%d" % (item_id) )
	    return

	rec_items = []
	sim_cat_ids = sim_cat_ids[0: self.strategy.get_max_sim_cat_process()]
	count = 0
	timer_total = Timer()
	for i in range(0, len(sim_cat_ids)):
	    (cat_id, sim_value) = sim_cat_ids[i]
	    sim_item_ids = self.cat_to_item_rindex.get(cat_id, [])
	    if len(sim_item_ids) == 0 : 
		write_log(sys._getframe().f_lineno, "cat_id:%d has no item" % (cat_id) )
		continue
	    timer = Timer()
	    count += len(sim_item_ids)
	    res_list = self.__find_sim_item_from_a_list(target_item, sim_item_ids, i)
	    write_log(msg = "__find_sim_item_from_a_list cost time:%f, sim_item_ids size:%d, i:%d" % (timer.get_diff(), len(sim_item_ids), i))
	    rec_items.extend(res_list)
	write_log(msg = "all__find_sim_item_from_a_list cost time:%f, all_sim_item_ids size:%d" % (timer_total.get_diff(), count))

	write_log(msg = 'process item_id:%d, rec_items size:%d' % (item_id, len(rec_items)) )
	rec_items.sort(lambda y,x : cmp(x[1], y[1]))
	rec_items = rec_items[0: self.strategy.get_total_rec_num()]

	final_res = []
	for (id, value) in rec_items:
	    final_res.append(id)

	return final_res

    def process(self, item_id):
	# 获得查询item的cat
	(cat_id, words) = self.dim_items_index.get(item_id, (-1, -1))
	if cat_id == -1 : return []

	# 获得这个cat的相似cat
	sim_cat_ids = self.cat_sim_rindex.get(cat_id, -1)
	if sim_cat_ids == -1 : return []

	write_log(msg = 'process item_id:%d, sim_cat_ids size:%d' % (item_id, len(sim_cat_ids)) )
	return self.__get_rec_item_ids(item_id, sim_cat_ids)



	



if __name__ == "__main__":
    input_filename == ''
    if sys.argc == 2:
	input_filename = sys.argv[1]

    print input_filename
    sys.exit(0)


    import common

    import dim_items_index_builder
    from dim_items_index_builder import *
    dim_items_index_builder = DimItemsIndexBuilder()
    dim_items_index_builder.build_from_file(common.dim_items_file)

    cat_to_item_rindex_builder = CatToItemRindexBuilder()
    cat_to_item_rindex_builder.build_from_file(common.dim_items_file)


    import cat_sim_builder
    from cat_sim_builder import *
    cat_sim_builder = CatSimBuilder(dim_items_index_builder.get_res())
    cat_sim_builder.build_from_file(common.dim_fashion_matchsets_file)

    cat_sim_rindex_builder = CatSimRindexBuilder()
    cat_sim = cat_sim_builder.get_res()
    cat_sim_rindex_builder.build_from_CatSimBuilder(cat_sim_builder)


    import word_iterm_base_builder
    from word_iterm_base_builder import *
    word_iterm_based_builder = WordItermBasedBuilder(dim_items_index_builder)
    word_iterm_based_builder.build_from_file(common.dim_fashion_matchsets_file)

    word_iterm_based_rindex_builder = WordItermBasedRindexBuilder()
    word_iterm_based_rindex_builder.build_from_WordItermBasedBuilder(word_iterm_based_builder)

    dim_items_index_builder.clear_notimportant_word_from_title(word_iterm_based_rindex_builder)

    #sys.exit(0)
    
    predictor = Predictor(dim_items_index_builder,
			  cat_to_item_rindex_builder,
			  cat_sim_builder,
			  cat_sim_rindex_builder,
			  word_iterm_based_builder)



    write_log(msg = 'begin predict')
    input_fd  = open(common.test_items_file)
    output_fd = open(common.res_test_items_file, 'w')
    for line in input_fd:
	item_id = (int)(line.strip())
	res = predictor.process(item_id)
	if len(res) > 0:
	    res_str = ",".join( map(str, res) )
	    print >> output_fd, "%d %s" % (item_id, res_str)
	else:
	    print >> output_fd, "%d" % item_id


