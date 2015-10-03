# -*- coding:utf-8-*-

# 创建item的正排信息
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
	    self.dim_item_index[item_id] = (cat_id, title_word_list_int)

    def get_res(self):
	return self.dim_item_index


if __name__ == "__main__":
    dim_items_index_builder = DimItemsIndexBuilder()

    filename = '../source_data/dim_items.txt'
    dim_items_index_builder.build_from_file(filename)
    dim_items_index = dim_item_index_builder.get_res()
    print dim_item_index

    for (k,v) in dim_item_index.items():
	print k,
	print " ",
	print v[0],
	print " ",
	print v[1]

	    
