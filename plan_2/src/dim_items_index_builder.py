# -*- coding:utf-8-*-

# 创建item的正排信息

from common import Item


class DimItemsIndexBuilder:
    def __init__(self):
	self.dim_item_index = {}
	pass

    def build_from_file(self, filename):
	fd = open(filename)

	for line in fd:
	    items = line.strip().split(' ')
	    if len(items) < 3 : continue

	    item_id = (int)(items[0])
	    cat_id = (int)(items[1])
	    title_word = items[2]
	    title_word_list = title_word.split(',')
	    title_word_list_int = []
	    for w in title_word_list : 
		title_word_list_int.append((int)(w))
	    self.dim_item_index[item_id] = Item(item_id=item_id, cat_id=cat_id, titles=title_word_list_int)


    def get_res(self):
	return self.dim_item_index

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
    import common
    from common import *
    import dim_items_index_builder
    from dim_items_index_builder import *
    dim_items_index_builder = DimItemsIndexBuilder()
    dim_items_index_builder.build_from_file(common.dim_items_file)
    #dim_items_index_builder.dump_to_file(common.dim_items_dump_file)



