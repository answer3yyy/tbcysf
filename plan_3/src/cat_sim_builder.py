# -*- coding:utf-8-*-
from common import Item


# 根据专家标注数据，生成 类目cat 之间的相似性
# 这里相似性的表征是 共现关系, 即两个 cat越经常被搭配，那么他们相似性越高
# 在衣着搭配上，相似性高并不意味这'很像',而是经常 共现
class CatSimBuilder:
    def __init__(self, cat_to_iterm_rindex):
	self.cat_to_iterm_rindex = cat_to_iterm_rindex
	self.cat_id_weight_list = []
	self.cat_to_cat_sim = {}

    def build_from_file(self, filename):
	fd = open(filename)

	for line in fd:
	    items = line.strip().split(' ')
	    if len(items) < 2 : continue
	    matchsets = items[1]

	    subsets_res = []
	    cat_subsets = matchsets.split(';')
	    for cat_set in cat_subsets:
		item_ids = cat_set.split(',')
		item_num = len(item_ids)
		if item_num < 1 : continue

		item_id = (int)(item_ids[0])
		weight = 1

		item = self.cat_to_iterm_rindex.get(item_id, -1)
		if item.cat_id == -1 : continue
		subsets_res.append((item.cat_id, weight))

	    if len(subsets_res) == 0: 
		continue
	    else: 
		self.cal_matrix(subsets_res)

    def cal_matrix(self, cat_id_weight_list):
	max_weight = 0
	for (cat_id, weight) in cat_id_weight_list:
	    if weight > max_weight : max_weight = weight

	l = len(cat_id_weight_list)
	for i in range(0, l):
	    (cat_id_i, weight_i) = cat_id_weight_list[i]
	    for j in range(i+1, l):
		(cat_id_j, weight_j) = cat_id_weight_list[j]

		key = (cat_id_i,cat_id_j)
	        weight = self.cat_to_cat_sim.get( (cat_id_i,cat_id_j), 0.0 )
		weight += (float)(weight_i + weight_j) / (float)(max_weight)

		self.cat_to_cat_sim[key] = weight

    def get_res(self):
	return self.cat_to_cat_sim


# 根据CatSimBuilder的结果建倒排索引
class CatSimRindexBuilder : 
    def __init__(self):
	self.cat_sim_rindex = {}
	pass

    def build_from_CatSimBuilder(self, cat_sim_builder):
	cat_sim = cat_sim_builder.get_res()

	for (key, weight) in cat_sim.items():
	    (cat1, cat2) = key

	    cat_list = self.cat_sim_rindex.get(cat1, [])
	    cat_list.append( (cat2, weight) )
	    self.cat_sim_rindex[cat1] = cat_list

	for (cat_id, cat_list) in self.cat_sim_rindex.items():
	    cat_list.sort(lambda x,y : cmp(y[1],x[1])) 
	    self.cat_sim_rindex[cat_id] = cat_list

    def dump_to_file(self, filename):
	fd = open(filename, 'w')
	for (cat_id, cat_list) in self.cat_sim_rindex.items():
	    print >> fd, cat_id
	    print >> fd, len(cat_list)
	    for (sim_cat_id, weight) in cat_list:
		print >> fd, "%d %d" % (sim_cat_id, weight)

    def get_res(self):
	return self.cat_sim_rindex






if __name__ == "__main__":
    import common
    import dim_items_index_builder
    from dim_items_index_builder import *
    dim_items_index_builder = DimItemsIndexBuilder()
    dim_items_index_builder.build_from_file(common.dim_items_file)
    dim_items_index = dim_items_index_builder.get_res()
    
    cat_sim_builder = CatSimBuilder(dim_items_index)
    cat_sim_builder.build_from_file(common.dim_fashion_matchsets_file)
    cat_sim = cat_sim_builder.get_res()

    cat_sim_rindex_builder = CatSimRindexBuilder()
    cat_sim_rindex_builder.build_from_CatSimBuilder(cat_sim_builder)
    cat_sim_rindex = cat_sim_rindex_builder.get_res()
    cat_sim_rindex_builder.dump_to_file(common.cat_sim_rindex_dump_file)
    print cat_sim_rindex
    print len(cat_sim_rindex)
    

