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
	cat = db.dim_items.find_one({"item":item})["cat"]#找出目录TODO这边可以优化，不止一个
	print cat
	simcatSet = db.dim_items.find({"cat":cat})
	print simcatSet[0]




if __name__ == '__main__':
	rec = "2232"#推荐商品
	totalItem = matchset()#专家标注
	matchJudge(rec,[])