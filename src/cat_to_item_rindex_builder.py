# -*- coding:utf-8-*-

from common import *
import common


# 创建cat到item的倒排索引
class CatToItemRindexBuilder :
    def __init__(self):
	self.cat_to_item_rindex = {}
	pass

    def build_from_file(self, filename):
	self.cat_to_item_rindex = {}
	fd = open(filename)

	for line in fd:
	    items = line.strip().split(' ')
	    if len(items) < 3: continue
	    item_id = (int)(items[0])
	    cat_id = (int)(items[1])

	    doc_list = self.cat_to_item_rindex.get(cat_id, [])
	    doc_list.append(item_id)
	    self.cat_to_item_rindex[cat_id] = doc_list


    def get_res(self):
	return self.cat_to_item_rindex


if __name__ == "__main__":
    cat_to_item_rindex_builder = CatToItemRindexBuilder()
    cat_to_item_rindex_builder.build_from_file(common.dim_items_file)







