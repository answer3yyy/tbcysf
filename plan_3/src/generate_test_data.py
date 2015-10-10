# -*- coding:utf-8 -*-

import sys
import common
from common import write_log
from common import Timer

import common
from common import *
import dim_items_index_builder
from dim_items_index_builder import *
from feature_builder import *
from sample_builder import *

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


strategy = Strategy()


if __name__ == "__main__":
    
    import dim_items_index_builder
    from dim_items_index_builder import *
    dim_items_index_builder = DimItemsIndexBuilder()
    dim_items_index_builder.build_from_file(common.dim_items_file)
    dim_items_index = dim_items_index_builder.get_res()
    print 'dim_items_index size:%d' % (len(dim_items_index))

    
    cat_to_item_rindex_builder = CatToItemRindexBuilder()
    cat_to_item_rindex_builder.build_from_file(common.dim_items_file)
    cat_to_item_rindex = cat_to_item_rindex_builder.get_res()

    import cat_sim_builder
    from cat_sim_builder import *
    cat_sim_builder = CatSimBuilder(dim_items_index_builder.get_res())
    cat_sim_builder.build_from_file(common.dim_fashion_matchsets_file)

    cat_sim_rindex_builder = CatSimRindexBuilder()
    cat_sim = cat_sim_builder.get_res()
    cat_sim_rindex_builder.build_from_CatSimBuilder(cat_sim_builder)
    cat_sim_rindex = cat_sim_rindex_builder.get_res()


    feature_builder = FeatureBuilder()
    for (item_id, item) in dim_items_index.items():
	item.pos = 1
	feature_builder.add_an_item(item)
	item.pos = 2
	feature_builder.add_an_item(item)
    print 'feature_builder item_feature_map size:%d' % (len(feature_builder.item_feature) )
    #print feature_builder.item_feature


    import test_builder
    from test_builder import *
    test_builder = TestBuilder(common.test_data_output, feature_builder, dim_items_index)

    input_fd  = open(common.test_items_file)
    for line in input_fd:
	item_id = (int)(line.strip())

	test_item = dim_items_index.get(item_id)
	if not test_item != None:
	    write_log(sys._getframe().f_lineno, "cannot get info of item_id:%d" % (item_id) )
	    continue

	sim_cat_ids = cat_sim_rindex.get(test_item.cat_id, -1)
	if sim_cat_ids == -1 : continue 


	sim_cat_ids = sim_cat_ids[0: strategy.get_max_sim_cat_process()]
	rec_items = []
	for i in range(0, len(sim_cat_ids)):

	    (cat_id, sim_value) = sim_cat_ids[i]
	    sim_item_ids = cat_to_item_rindex.get(cat_id, [])
	    if len(sim_item_ids) == 0 : 
		write_log(sys._getframe().f_lineno, "cat_id:%d has no item" % (cat_id) )
		continue

	    count = 0
	    for sim_id in sim_item_ids:
		count += 1
		if count > 1000 : break
		test_builder.create_a_test(test_id = item_id, match_id = sim_id)

	 


