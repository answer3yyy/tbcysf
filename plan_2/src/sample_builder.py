# -*- coding:utf-8 -*-
from common import Item
from common import write_log
from distribute import Distribute


class SampleBuilder:
    def __init__(self, output_file, feature_builder, dim_items_index):
	self.outfd = open(output_file, 'w')
	self.feature_builder = feature_builder
	self.dim_items_index = dim_items_index
	self.sample_feature_map = {}
	self.sample_feature_total_len = 0
	self.pos_fea_id = set()
	self.dis = Distribute()
	pass

    def __add_to_dis(self, fea):
	for id in fea:
	    self.dis.add(id)

    def __add_to_map(self, fea, target):
	self.sample_feature_map[str(fea)] = target
	self.sample_feature_total_len += len(fea)

    def __print_feature(self, fea, target):

	out_str = "%d " %(target)
	for fid in fea:
	    out_str += "%d:1 " % (fid)
	#print out_str.strip()
	print >> self.outfd, out_str.strip()

    def __create_a_sample(self, item_id_a, item_id_b):

	item_a = self.dim_items_index.get(item_id_a, None)
	if not item_a != None: 
	    write_log(msg = '__create_a_sample get no item, id:%d' % item_id_a)
	    return

	item_b = self.dim_items_index.get(item_id_b, None)
	if not item_b != None:
	    write_log(msg = '__create_a_sample get no item, id:%d' % item_id_a)
	    return

	item_a.pos = 1
	item_b.pos = 2
	fea_a = self.feature_builder.get_feature(item_a)
	fea_b = self.feature_builder.get_feature(item_b)
	fea = fea_a + fea_b
	if len(fea) == 0 : write_log(msg = 'fea len is 0, item_id %d %d' % (item_id_a, item_id_b) )
	fea = sorted(fea)
	self.__add_to_dis(fea)
	self.__add_to_map(fea, 1)
	self.__print_feature(fea, 1)


	item_a.pos = 2
	item_b.pos = 1
	fea_a = self.feature_builder.get_feature(item_a)
	fea_b = self.feature_builder.get_feature(item_b)
	fea = fea_a + fea_b
	fea = sorted(fea)
	self.__add_to_dis(fea)
	self.__add_to_map(fea, 1)
	self.__print_feature(fea, 1)

    def get_sample_fea_average(self):
	return self.sample_feature_total_len / len(self.sample_feature_map)


    def process_a_line(self, line):
	items = line.strip().split(' ')
	if len(items) < 2 : return

	match_group = items[1]
	match_cats = match_group.split(';')

	for i in range(0, len(match_cats)):
	    tmp_list = map(int, match_cats[i].split(','))
	    match_cats[i] = tmp_list

	for i in range(0, len(match_cats)):
	    for j in range(i+1, len(match_cats)):
		if i == j: continue

		groups_a = match_cats[i]
		groups_b = match_cats[j]

		for item_a in groups_a:
		    for item_b in groups_b:
			# item_a and item_b are item id 
			self.__create_a_sample(item_a, item_b)


    def build_from_file(self, filename):
	infd = open(filename)
	for line in infd:
	    self.process_a_line(line)



    def add_negative(self, negative_num = -1, positive_num = -1, max_fea_id = -1):
	if positive_num == -1 : positive_num = len(self.sample_feature_map)
	if negative_num == -1 : negative_num = positive_num * 10
	if max_fea_id   == -1 : max_fea_id = self.feature_builder.feature_id_count

	import random
	average_sample_fea_len = self.get_sample_fea_average()

	pos_fea_id_list = list(self.pos_fea_id)
	pos_fea_id_num = len(pos_fea_id_list)
	print 'pos_fea_id_num : %d' % (pos_fea_id_num)
	print 'positive_num : %d' % (positive_num)
	print 'negative_num : %d' % (negative_num)
	print 'max_fea_id : %d' % (max_fea_id)
	print 'average_sample_fea_len : %d' %(average_sample_fea_len)

	self.dis.build()

	for i in range(0, negative_num):
	    target_len = random.randrange(0, average_sample_fea_len) + average_sample_fea_len/2

	    fea = []
	    for j in range(0, target_len):
		id = self.dis.gen_rand()
		fea.append(id)

	    fea = set(fea)
	    while len(fea) < target_len:
		id = self.dis.gen_rand()
		if id in fea: continue
		fea.add(id)

	    fea = sorted(list(fea))
	    key = str(fea)
	    if not self.sample_feature_map.has_key(key):
		self.__add_to_map(fea, 0)
		self.__print_feature(fea, 0)



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

    sample_builder = SampleBuilder(common.sample_data_output, feature_builder, dim_items_index)
    #line = '1 1,2;3'
    #sample_builder.process_a_line(line)
    fd = open(common.dim_fashion_matchsets_file)
    for line in fd: sample_builder.process_a_line(line)

    print sample_builder.sample_feature_map

    
    sample_builder.add_negative()


