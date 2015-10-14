#coding:utf-8
import idata
import json
import time

def matchJudge(item_a,item_b,item_title,item_image):
	if item_title.has_key(item_a) and item_image.has_key(item_a):
		if item_title.has_key(item_b) and item_image.has_key(item_b):
			image_side = sum([1 for i in xrange(len(item_image[item_a])) if item_image[item_a][i]!=item_image[item_b][i]])
			if item_title[item_a]["cat"] == item_title[item_b]["cat"]:
				cat_side = 1
			else:
				cat_side = 0
			temp_a = set(item_title[item_a]["title"])
			temp_b = set(item_title[item_b]["title"])
			title_side = 1.0*len(temp_a & temp_b)/len(temp_a | temp_b)
			#print "****"
			#print temp_a,temp_b
			#print title_side
			return (image_side,cat_side,title_side)
		else:
			return "b can not be found"
	return "a can not be found"

def test_matchJudge(item_title,item_image):
	item_match = idata.dim_matchsets_sim()[0:100]
	d = []
	for i in xrange(len(item_match)):
		d.append(matchJudge(item_match[i][0],item_match[i][1],item_title,item_image))
	with open("G:\\dev\\tianchi\\data\\matchjudge.json", "w") as f:
		json.dump(d, f)



if __name__ == '__main__':
	rec = "2232"#推荐商品
	item_title = idata.dim_item_title()#{"XXX":{"title":[],"cat":"xxx"}}
	#print item_title
	item_image = idata.dim_item_image()#{"XXX":"00101010010"}
	#print item_image
	item = idata.dim_matchsets_total()
	#test_matchJudge(item_title,item_image)#测试相似性
	item_match_sim = idata.dim_item_match_sim()#{"xxx":{matchset:[],simset:[]}}
	#print len(item),len(item_match_sim)
	print "data ready!"
	cat = item_title[rec]["cat"]
	print cat
	candidate = []
	time1 = time.time()
	for i in item:
		temp = matchJudge(rec,i,item_title,item_image)

		if temp[1] == 1:
			if temp[2] > 0.2:
				candidate.append((i,temp[2],temp[0]))
		#break
	print candidate
	print len(candidate)
	time2 = time.time()
	print str(time2-time1)
	candidate = sorted(candidate,key=lambda candidate_tuple:candidate_tuple[1],reverse=1)[0:3]#提取三个
	print candidate
	sim_candidate = []#映射过去的集合
	for ii in candidate:
		if item_match_sim.has_key(ii[0]):
			temp = item_match_sim[ii[0]]["matchset"]
			for i in temp:
				sim_candidate.append((i,ii[1]))
	print sim_candidate
	result = []#最后结果
	for i in sim_candidate:
		for j in item:
			temp = matchJudge(i[0],j,item_title,item_image)
			if temp[1] ==1:
				if temp[2] > 0.2:
					result.append((j,1.0*temp[2]*i[1]))
	result = sorted(result,key=lambda result_tuple:result_tuple[1],reverse=1)[0:200]
	print result






