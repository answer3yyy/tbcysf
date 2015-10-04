import pymongo
import codecs
conn = pymongo.Connection(host="127.0.0.1",port=27017)
db = conn.tianchi
#db.test.insert({"test":"test"})
#db.test.update({"test":"test"},{"$set":{"name":"haha"}})

#print list(db.user.find())
def txt2db1():
	f = codecs.open("G:\\dev\\tianchi\\data\\dim_items\\dim_items.txt","r").readlines()
	print f[1].split()
	for i in xrange(1,len(f)):
		itemTemp = f[i].split()
		#print type(itemTemp[0])
		dic = {"item":itemTemp[0],"cat":itemTemp[1],"title":itemTemp[2].split(u",")}
		#print dic
		db.dim_items.insert(dic)
		#break
	print "done"

def image_feature2db():
	f = codecs.open("G:\\dev\\tianchi\\data\\item_images_feature","r").readlines()
	for i in xrange(len(f)):
		item = f[i].split()
		#print type(item[0])
		db.dim_items.update({"item":item[0]},{"$set":{"image":item[1]}})
		print i*1.0/len(f)

def match2db():
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
	#print totalItem[0:10]
	#print len(totalItem)
	for i in totalItem:
		print i
		f = codecs.open("G:\\dev\\tianchi\\data\\dim_fashion_matchsets.txt","r").readlines()
		for j in xrange(len(f)):
			f[j] = f[j].split()[1]
			if i in f[j]:
				print f[j]
		break






if __name__ == '__main__':
	#txt2db1()
	#image_feature2db()
	match2db()