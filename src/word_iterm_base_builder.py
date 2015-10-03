import sys

class WordItermBasedBuilder:
    def __init__(self, dim_item_index_builder):
	self.dim_item_index = dim_item_index_builder.get_res()
	self.word_iterm_based = {}
	pass

    def __process_line_word_matrix(self, all_cat_word):
	for i in range(0, len(all_cat_word)):
	    cat_word_i = all_cat_word[i]
	    for word_i in cat_word_i:
		for j in range(i+1, len(all_cat_word)):
		    if i == j : continue
		    cat_word_j = all_cat_word[j]
		    for word_j in cat_word_j:
			if word_i == word_j : continue
			
			key = (word_i, word_j)
			weight = self.word_iterm_based.get(key, 0)
			weight += 1
			self.word_iterm_based[key] = weight
			
			key = (word_j, word_i)
			weight = self.word_iterm_based.get(key, 0)
			weight += 1
			self.word_iterm_based[key] = weight


    def __process_line(self, line):
	items = line.strip().split(' ')
	if len(items) < 2 : return

	match_group = items[1]
	match_cats = match_group.split(';')
	
	all_cat_word = []
	for a_cat in match_cats :
	    cat_word = []
	    items = a_cat.strip().split(',')
	    for item_id in items:
		item_id = (int)(item_id)
		index_info = self.dim_item_index.get(item_id, 0)
		if index_info == 0 : continue
		else:
		    item_word_list = index_info[1]
		    cat_word.extend(item_word_list)
	    cat_word = list(set(cat_word))
	    all_cat_word.append(cat_word)
	self.__process_line_word_matrix(all_cat_word)


    def build_from_file(self, filename):
	fd = open(filename)
	for line in fd:
	    self.__process_line(line)

    def get_res(self):
	return self.word_iterm_based
    
    


	
if __name__ == "__main__":
    import common
    from dim_items_index_builder import *
    dim_item_index_builder = DimItemsIndexBuilder()
    dim_item_index_builder.build_from_file(common.dim_items_file)

    word_iterm_based_builder = WordItermBasedBuilder(dim_item_index_builder)
    word_iterm_based_builder.build_from_file(common.dim_fashion_matchsets_file)
    word_iterm_based = word_iterm_based_builder.get_res()
    print word_iterm_based



