import codecs

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
			if item in f[j]:
				#print f[j]
				seqList.append(f[j])
		resultSetTemp = matchFix_(item,seqList)
		#print resultSetTemp
		resultSet[item] = resultSetTemp
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
					print simsetTemp
					print item
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
	totalItem,resultSet = matchFix()
	print resultSet