
class DimItemsIndexBuilder:
    def get_res():
	return { 
		 1 : (1, []),
		 2 : (2, []),
		 3 : (3, []),
		 4 : (1, []),
		 5 : (2, []),
		 6 : (3, []),
		 7 : (1, [])
	       }

dim_items_index_builder = DimItemsIndexBuilder()



class CatToItemRindexBuilder:
    def get_res():
	return {
		 1: [1, 4, 7],
		 2: [2, 5],
		 3: [3, 6]
	       }
cat_to_item_rindex_builder = CatToItemRindexBuilder()


class CatSimBuilder:
    def get_res():
	return {

	       }
cat_sim_builder = CatSimBuilder()
