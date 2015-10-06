import codecs
import pymongo
conn = pymongo.Connection(host="127.0.0.1",port=27017)
db = conn.tianchi

def matchFix():
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
	resultSet = {}
	for item in totalItem:
		#print item
		seqList = []
		f = codecs.open("G:\\dev\\tianchi\\data\\dim_fashion_matchsets.txt","r").readlines()
		for j in xrange(len(f)):
			f[j] = f[j].split()[1]
			jTemp = ";".join(f[j].split(u","))
			jList = jTemp.split(u";") 
			if item in jList:
				#print f[j]
				#print jList
				seqList.append(f[j])
		resultSetTemp = matchFix_(item,seqList)
		set2db = {"item":item,"simset":resultSetTemp["simset"],"matchset":resultSetTemp["simset"]}
		#print set2db
		db.dim_fashion_matchsets.insert(set2db)
		resultSet[item] = resultSetTemp
		#print resultSet
		#print resultSet
		#break
	return totalItem,resultSet

def matchFix_(item,itemSeqList):
	matchset = []
	simset = []
	for itemSeq in itemSeqList:
		if item in itemSeq:
			#print '###'
			seqTemp = itemSeq.split(u";")
			#print seqTemp
			for i in seqTemp:
				#print i
				if u"," in i and item in i:
					simsetTemp = i.split(u",")
					#print simsetTemp
					#print item
					simsetTemp.remove(item)
					simset.extend(simsetTemp)
					break
			matchsetTemp = []
			for i in seqTemp:
				if item not in i and u"," not in i:
					matchsetTemp.append(i)
				if item not in i and u"," in i:
					matchsetTemp.extend(i.split(u","))
			matchset.extend(matchsetTemp)
	resultSet = {"matchset":matchset,"simset":simset}
	return resultSet









if __name__ == '__main__':
	rec = "2232"
	totalItem,resultSet = matchFix()
	print resultSet