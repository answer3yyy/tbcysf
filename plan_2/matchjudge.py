#coding:utf-8
import codecs
import pymongo
conn = pymongo.Connection(host="127.0.0.1",port=27017)
db = conn.tianchi
import idata

def matchset():
	f = codecs.open("G:\\dev\\tianchi\\data\\dim_fashion_matchsets.txt","r").readlines()
	totalItem = []
	for i in xrange(len(f)):
		f[i] = f[i].split()[1]
		f[i] = f[i].split(u";")
		for j in f[i]:
			if u"," not in j:
				totalItem.append(j)
			else:
				j = j.split(u",")
				for k in j:
					totalItem.append(k)
	totalItem = list(set(totalItem))
	return totalItem

def matchJudge(item,matchList,num = 200):
	item = db.dim_items.find_one({"item":item})#找出目录TODO这边可以优化，不止一个
	print item
	candidate = []
	for i in matchList:
		temp = db.dim_items.find_one({"cat":item["cat"],"item":i})
		#print temp
		if str(temp) != "None":
			candidate.append(temp)
	print candidate
	for i in candidate:
		print judgeMethod(item,i)
	#print simcatSet[1]
	#print len(list(simcatSet))

def judgeMethod(item_a,item_b):#需要测试啊TODO
	index = 0#评价相似性指数0~100
	if item_a.has_key("image") and item_b.has_key("image"):
		image_side = sum([1 for i in xrange(len(item_a["image"])) if item_a["image"][i]!=item_b["image"][i]])
	else:
		image_side = 64
	#test
	'''
	a = "11010"
	b = "01111"
	image_side = sum([1 for i in xrange(len(a)) if a[i]!=b[i]])
	print image_side
	a = set(["a","b","c"])
	b = set(["b","c","d"])
	title_side = 1.0*len(a & b)/len(a | b)
	print title_side
	'''
	if item_a.has_key("title") and item_b.has_key("title"):
		temp_a = set(item_a["title"])
		temp_b = set(item_b["title"])
		title_side = 1.0*len(temp_a & temp_b)/len(temp_a | temp_b)
	else:
		title_side = 0.0
	if image_side <= 5:
		index = 100
	elif image_side <=10:
		index = 100*title_side
	else:
		index = image_side*title_side
	return index







if __name__ == '__main__':
	rec = "2232"#推荐商品
	#totalItem = matchset()#专家标注
	#matchJudge(rec,totalItem)
	#judgeMethod([],[])