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
    
    def dump_to_file(self, filename):
	fd = open(filename, 'w')
	for (item_id, v) in self.dim_item_index.items():
	    print >> fd, item_id
	    print >> fd, v[0]
	    print >> fd, len(v[1])
	    print >> fd, " ".join( map(str, v[1]) )

    def clear_notimportant_word_from_title(self, word_iterm_base_rindex_builder):
	word_iterm_base_rindex = word_iterm_base_rindex_builder.get_res()
	for (item_id, value) in self.dim_item_index.items():
	    (cat, title_list) = value

	    new_title = []
	    for w in title_list:
		if word_iterm_base_rindex.has_key(w):
		    new_title.append(w)

	    #if len(new_title) < len(title_list):
	    #	self.dim_item_index[item_id] = (cat, new_title)
	    if len(new_title) > 5: 
		new_title = new_title[0:5]
	    self.dim_item_index[item_id] = (cat, new_title)




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

    def dump_to_file(self, filename):
	fd = open(filename, 'w')
	for (k,doclist) in self.cat_to_item_rindex.items():
	    cat_id = k
	    item_num = len(doclist)
	    print >> fd, cat_id
	    print >> fd, item_num
	    for item in doclist:
		print >>fd, item


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

    cat_to_item_rindex_builder = CatToItemRindexBuilder()
    cat_to_item_rindex_builder.build_from_file(common.dim_items_file)
    cat_to_item_rindex_builder.dump_to_file(common.cat_to_item_rindex_dump_file)







