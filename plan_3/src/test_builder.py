
from common import Item
from common import write_log




class TestBuilder:
    def __init__(self, output_file, feature_builder, dim_items_index):
	self.outfd = open(output_file, 'w')
	self.feature_builder = feature_builder
	self.dim_items_index = dim_items_index
	pass

    def __add_to_pos_fea_id(self, fea):
	fea = set(fea)
	for id in fea:
	    if not id in self.pos_fea_id:
		self.pos_fea_id.add(id)

    def __add_to_map(self, fea, target):
	self.sample_feature_map[str(fea)] = target
	self.sample_feature_total_len += len(fea)

    def __print_feature(self, test_id, match_id, fea):

	out_str = ""
	for fid in fea:
	    out_str += "%d:1 " % (fid)
	print >> self.outfd, "%d,%d#%s" % (test_id, match_id, out_str.strip())

    def create_a_test(self, test_id, match_id):

	test_item = self.dim_items_index.get(test_id, None)
	if not test_item != None: 
	    write_log(msg = '__create_a_test get no item, id:%d' % test_id)
	    return

	match_item = self.dim_items_index.get(match_id, None)
	if not match_item != None:
	    write_log(msg = '__create_a_test get no item, id:%d' % match_id)
	    return

	test_item.pos = 1
	match_item.pos = 2
	fea_a = self.feature_builder.get_feature(test_item)
	fea_b = self.feature_builder.get_feature(match_item)
	fea = fea_a + fea_b
	if fea == None or len(fea) == 0 : write_log(msg = 'fea len is 0, item_id %d %d' % (test_id, match_id) )
	fea = sorted(fea)
	self.__print_feature(test_id, match_id, fea)
	return fea


    
if __name__ == "__main__":

    import common
    from common import Item
    from feature_builder import *
    feature_builder = FeatureBuilder()

    item1 = Item(1, 16, [2,3,4], 1)
    feature_builder.add_an_item(item1)
    item1.pos = 2
    feature_builder.add_an_item(item1)
    item2 = Item(2, 15, [2,3,4], 1)
    feature_builder.add_an_item(item2)
    item2.pos = 2
    feature_builder.add_an_item(item2)
    item3 = Item(3, 17, [2,7,4], 1)
    feature_builder.add_an_item(item3)
    item3.pos = 2
    feature_builder.add_an_item(item3)


    dim_items_index = { item1.item_id:item1, item2.item_id:item2, item3.item_id:item3 }

    test_builder = TestBuilder(common.sample_data_output, feature_builder, dim_items_index)
    print test_builder.create_a_test(2, 3)
