#coding:utf-8
import codecs
import json
def dim_item_title():
	#商品item,cat,title
	f = codecs.open("G:\\dev\\tianchi\\data\\dim_items\\dim_items.txt","r").readlines()
	#print f[1].split()
	temp = []
	for line in f:
		line = line.replace("\r\n","")
		line = line.replace("\n","")
		temp.append(line)
	f = temp
	dim_item_title = {}
	for i in xrange(1,len(f)):
		itemTemp = f[i].split()
		#print type(itemTemp[0])
		dim_item_title[itemTemp[0]] = {"cat":itemTemp[1],"title":itemTemp[2].split(u",")}
		#print dim_item_title
		#break
	return dim_item_title

def dim_item_image():
	#商品item,image
	f = codecs.open("G:\\dev\\tianchi\\data\\item_images_feature","r").readlines()
	dim_item_image = {}
	for i in xrange(len(f)):
		item = f[i].split()
		dim_item_image[item[0]] = item[1] 
	return dim_item_image

def dim_matchsets_total():
	#相似集合里面所有item集合
	f = codecs.open("G:\\dev\\tianchi\\data\\dim_fashion_matchsets.txt","r").readlines()
	temp = []
	for line in f:
		line = line.replace("\r\n","")
		line = line.replace("\n","")
		temp.append(line)
	f = temp
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

def dim_matchsets_sim():
	#相似集合里面所有相似的元素(a,b)
	f = codecs.open("G:\\dev\\tianchi\\data\\dim_fashion_matchsets.txt","r").readlines()
	dataset = []
	temp = []
	for line in f:
		line = line.replace("\r\n","")
		line = line.replace("\n","")
		temp.append(line)
	f = temp
	for i in xrange(len(f)):
		f[i] = f[i].split()[1]
		if u"," in f[i]:
			temp = f[i].split(u";")
			for j in temp:
				if u"," in j:
					dataset.append(j.split(u","))
	temp = dataset
	dataset = []
	for i in xrange(len(temp)):
		dataset.extend(dim_matchsets_sim_fix(temp[i]))
	return dataset

def dim_item_match_sim():
	with open("G:\\dev\\tianchi\\data\\dim_fashion_matchsets.json", "r") as f:
		d = json.load(f)
	return d

def matchFix():
	f = codecs.open("G:\\dev\\tianchi\\data\\dim_fashion_matchsets.txt","r").readlines()
	temp = []
	for line in f:
		line = line.replace("\r\n","")
		line = line.replace("\n","")
		temp.append(line)
	f = temp
	totalItem = []
	for i in xrange(len(f)):
		f[i] = f[i].split()[1]
		f[i] = f[i].split(u";")
		f[i] = ','.join(f[i])
		f[i] = f[i].split(u",")
		totalItem.extend(f[i])
	totalItem = list(set(totalItem))
	#print totalItem[0:10]
	#print len(totalItem)
	resultSet = {}
	for item in totalItem:
		#print item
		seqList = []
		f = codecs.open("G:\\dev\\tianchi\\data\\dim_fashion_matchsets.txt","r").readlines()
		temp = []
		for line in f:
			line = line.replace("\r\n","")
			line = line.replace("\n","")
			temp.append(line)
		f = temp
		#print f
		for j in xrange(len(f)):
			f[j] = f[j].split()[1]
			jTemp = ",".join(f[j].split(u";"))
			jList = jTemp.split(u",") 
			if item in jList:
				#print f[j]
				#print jList
				seqList.append(f[j])
		#print seqList
		resultSetTemp = matchFix_(item,seqList)
		resultSet[item] = resultSetTemp
		#print resultSet
		#print resultSet
		#break
	return resultSet



#----------------------------------------------------------------------------------------
def dim_matchsets_sim_fix(dataset = ["a","b"]):
	if len(dataset) == 2:
		return [(dataset[0],dataset[1])]
	else:
		result = []
		for i in xrange(len(dataset)):
			for j in xrange(i+1,len(dataset)):
				result.append((dataset[i],dataset[j]))
		return result

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
					try:
						simsetTemp.remove(item)
					except:
						print item,simsetTemp
					simset.extend(simsetTemp)
					break
			matchsetTemp = []
			for i in seqTemp:
				if item not in i and u"," not in i:
					matchsetTemp.append(i)
				if item not in i and u"," in i:
					matchsetTemp.extend(i.split(u","))
			matchset.extend(matchsetTemp)
	resultSet = {"matchset":list(set(matchset)),"simset":list(set(simset))}
	return resultSet

if __name__ == '__main__':
	#print dim_item_title()
	#print dim_item_image()["1911791"]
	#print dim_matchsets_sim()
	import time
	time1 = time.time()
	d =  matchFix()
	#print d
	with open("G:\\dev\\tianchi\\data\\dim_fashion_matchsets.json", "w") as f:
		json.dump(d, f)
	time2 = time.time()
	print str(time2-time1)
