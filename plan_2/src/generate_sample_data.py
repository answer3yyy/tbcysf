import common
from common import *
import dim_items_index_builder
from dim_items_index_builder import *
from feature_builder import *
from sample_builder import *


if __name__ == "__main__":
    
    dim_items_index_builder = DimItemsIndexBuilder()
    dim_items_index_builder.build_from_file(common.dim_items_file)
    dim_items_index = dim_items_index_builder.get_res()
    print 'dim_items_index size:%d' % (len(dim_items_index))

    feature_builder = FeatureBuilder()
    for (item_id, item) in dim_items_index.items():
	item.pos = 1
	feature_builder.add_an_item(item)
	item.pos = 2
	feature_builder.add_an_item(item)
    print 'feature_builder item_feature_map size:%d' % (len(feature_builder.item_feature) )


    sample_builder = SampleBuilder(common.sample_data_output, feature_builder, dim_items_index)
    fd = open(common.dim_fashion_matchsets_file)
    for line in fd:
	sample_builder.process_a_line(line)

    sample_builder.add_negative()

