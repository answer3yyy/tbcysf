#coding:utf-8
import idata

if __name__ == '__main__':
	rec = "2232"#推荐商品
	item_title = idata.dim_item_title()#{"XXX":{"title":[],"cat"}}
	#print item_title
	item_image = idata.dim_item_image()#{"XXX":"00101010010"}
	#print item_image
	item = idata.dim_matchsets_total()
	print "dataloaded!!"

	
	print item_title[rec]
	print item_image[rec]