# -*- coding:utf-8 -*-
from common import Item
from common import write_log
from bisect import bisect_left

# 用来记录正样本的分布，在产生负样本时，根据这个分布来产生
class Distribute:
    def __init__(self):
	self.max = 0
	self.min = 999999
	self.fea_map = {}
	self.num = 0
	self.max_idx = 0

	self.idx_to_id = []
	self.idx_acu_sum = []



    def add(self, id):
	if id > self.max : self.max = id
	if id < self.min : self.min = id

	c = self.fea_map.get(id, 0)
	self.fea_map[id] = ( c + 1 )
	self.num += 1

    def build(self):
	self.idx_acu_sum = []
	self.idx_acu_sum = []
	sum = 0
	for (id, c) in self.fea_map.items():
	    sum += c
	    self.idx_acu_sum.append(sum)
	    self.idx_to_id.append(id)
	self.max_idx = len(self.idx_to_id) - 1

    def gen_rand(self):
	import random
	r = random.randrange(0, self.num)
	pos = bisect_left(self.idx_acu_sum, r)  

	if pos > self.max_idx : pos -= 1
	if pos < 0 : pos = 0
	
	return self.idx_to_id[pos]

    def get_id_list(self):
	return self.idx_to_id

if __name__ == "__main__":
    dis = Distribute()

    for i in range(0, 10) : dis.add(1)
    for i in range(0, 20) : dis.add(2)
    for i in range(0, 30) : dis.add(3)
    for i in range(0, 40) : dis.add(4)


    self.dis.build()

    mp = {}
    for i in range(0, 10000):
	r = dis.gen_rand()
	n = mp.get(r, 0)
	mp[r] = n+1

    for (k, v) in mp.items():
	print k,v
