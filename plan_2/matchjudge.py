#coding:utf-8
import codecs
import pymongo
conn = pymongo.Connection(host="127.0.0.1",port=27017)
db = conn.tianchi


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
		print temp
		candidate.append(temp)
	print candidate
	#print simcatSet[1]
	#print len(list(simcatSet))

def judgeMethod(item_a,item_b):
	a = "11010"
	b = "01111"
	image_side = sum([1 for i in xrange(len(a)) if a[i]!=b[i]])
	print image_side
	a = set(["a","b","c"])
	b = set(["b","c","d"])
	title_side = 1.0*len(a & b)/len(a | b)
	print title_side






if __name__ == '__main__':
	rec = "2232"#推荐商品
	totalItem = matchset()#专家标注
	#matchJudge(rec,["41","456"])
	judgeMethod([],[])