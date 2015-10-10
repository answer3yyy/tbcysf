

class FeatureBuilder:
    def __init__(self):
	self.feature_map = {}
	self.feature_rmap = {}
	self.item_feature = {}
	self.feature_id_count = 0
	pass

    def __process_a_key(self, feature_key):
        fid = self.feature_map.get(feature_key, -1)
        if fid == -1: 
	    self.feature_id_count += 1
	    fid = self.feature_id_count
	    self.feature_map[feature_key] = fid
	    self.feature_rmap[fid] = feature_key
	return fid

    def __item_to_keys(self, item):
	pos = item.pos
	keys = []
	keys.append( "c_%d_%d" % (pos, item.cat_id) )
	for w in item.titles:
	    keys.append( "w_%d_%d" % (pos, w) )
	return keys



    def add_an_item(self, item):
	keys = self.__item_to_keys(item)
	feature = []
	for k in keys:
	    fid = self.__process_a_key(k)
	    feature.append(fid)
	feature = list(set(feature))

	#print 'add map key:%s  value:%s' % (item.hash_str(), str(feature) )
	self.item_feature[item.hash_str()] = feature
	return feature

    def get_feature(self, item):
        #print 'get map key:%s' % (item.hash_str())
	return self.item_feature.get(item.hash_str(), [])


	
if __name__ == "__main__":
    from common import Item
    feature_builder = FeatureBuilder()

    item1 = Item(1, 16, [2,3,4], 2)
    print feature_builder.add_an_item(item1)

    item2 = Item(2, 15, [2,3,4], 1)
    print feature_builder.add_an_item(item2)

    item3 = Item(1, 17, [2,7,4], 2)
    print feature_builder.add_an_item(item3)

    item4 = Item(1, 17, [2,7,4], 2)
    print feature_builder.get_feature(item4)

