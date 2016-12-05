import json
import string
import time
import numpy as np
import pandas as pd

temp = open('review2analysis.json','r')
reviews = json.load(temp)

ntemp = open('dishname.json','r')
dish_name = json.load(ntemp)

ttemp = open('dishtree.json','r')
dish_tree = json.load(ttemp)



restaurant = {}
restaurant_info = {}
raw_result = {}
result = {}
author = {}

for item in reviews:
	#print reviews[item][0]['keyword']
	name = reviews[item][0]['restaurant']
	author_name = reviews[item][0]['author']
	review_time = reviews[item][0]['time']
	if restaurant.has_key(name) == False:
		restaurant[name] = {}
	if author.has_key(author_name) == False:
		author[author_name] = []
	
	#restaurant[reviews[item][0]['restaurant']]
	#score = 0.0
	for review in reviews[item]:
		#print name, review['keyword'], review['result']['score']
		if restaurant[name].has_key(review['keyword']) == False:
			restaurant[name][review['keyword']] = []
		temp = []

		score = float(review['result']['score'])
		#author = author_name
		temp.append(score)
		temp.append(author_name)
		temp.append(review_time)
		restaurant[name][review['keyword']].append(temp)
		author[author_name].append(score)
		#if review['keyword'] == 'salad':
			#print review, score

#reataurant:
#{u'masago': [[0.51759, u'Tasmia A.', u'2016-08-12']], 
# u'roll': [[0.51759, u'Tasmia A.', u'2016-08-12'], 
# 		  [0.719549, u'Hugo G.', u'2016-02-20']], 
# u'sashimi': [[0.611502, u'Greg T.', u'2015-04-15']]}



#get score from restaurant
for item in restaurant:
	raw_result[item] = {}
	for key in restaurant[item]:
		if raw_result[item].has_key(key) == False:
			raw_result[item][key]=0.0
		#print restaurant[item][key]
		temp = 0.0
		s_count = 0
		for s in restaurant[item][key]:
			temp += s[0]
			s_count += 1
		raw_result[item][key] = temp/s_count
	
#for item in raw_result:
#	print item, raw_result[item]


#author
author_result = {}
author_analysis = np.zeros(20)

for item in author:
	temp = np.array(author[item]).mean()
	ana_temp = int(temp * 10)
	
	#print ana_temp
	author_result[item] = ana_temp + 9
	#print ana_temp + 9
	author_analysis[ana_temp+9] += 1

#for item in author_result:
#	print author_result[item]

for i in range(len(author_analysis)):
	author_analysis[i] = author_analysis[i]/author_analysis.sum()

for item in restaurant:
	for dish in restaurant[item]:
		temp_author = restaurant[item][dish][0][1]
		index = author_result[temp_author]
		if author_analysis[index] < 0.05:
			#print author_analysis[index]
			restaurant[item][dish][0][0] *= 0.5


#time
time_total = 0
time_9 = 0
time_8 = 0
time_5 = 0
times = []
for item in restaurant:
	for dish in restaurant[item]:
		t = restaurant[item][dish][0][2]
		ttemp = pd.Timestamp(t)
		times.append(ttemp)
#		print ttemp
		time_total += 1
		if ttemp < pd.Timestamp('2016-6-30') and ttemp > pd.Timestamp('2016-4-1'):
			restaurant[item][dish][0][0] *= 0.9
			time_9 += 1
		elif ttemp < pd.Timestamp('2016-3-31') and ttemp > pd.Timestamp('2015-10-1'):
			restaurant[item][dish][0][0] *= 0.8
			time_8 += 1
		elif ttemp < pd.Timestamp('2015-9-30'):
			restaurant[item][dish][0][0] *= 0.5
			time_5 += 1
#			print "find!"
	#print restaurant[item]

print time_total, time_9, time_8, time_5

#get adjusted score from restaurant
for item in restaurant:
	result[item] = {}
	for key in restaurant[item]:
		if result[item].has_key(key) == False:
			result[item][key]=0.0
		#print restaurant[item][key]
		temp = 0.0
		s_count = 0
		for s in restaurant[item][key]:
			temp += s[0]
			s_count += 1
		result[item][key] = temp/s_count



#dish_link_list = {}
#count_root = 0
#count_leaf = 0
#for item in dish_tree:
#	count_root += 1
#	count_leaf += len(dish_tree[item])
#	#print item, len(dish_tree[item])
#print count_root, count_leaf, count_leaf / count_root

count_res = 0
count_dish = 0
	
for item in result:
	count_res += 1
	count_dish += len(result[item])
	#print len(result[item])
print count_res, count_dish, count_dish/count_res
#	for temp in result[item]:
#		print temp, result[item][temp], raw_result[item][temp]

times = sorted(times)
for item in times:
	print item


#print len(dish_tree)
#print len(dish_name)
#print len(restaurant)

#for item in result:
	#print item
	#print result[item]
	#for key in result[item]:
		#print key
		#print result[item][key]


	#print item, len(reviews[item]), score / len(reviews[item])
	#restaurant[name][item] = score / len(reviews[item])
#for item in dish_tree:
#	for key in dish_tree[item]:
#		name = dish_tree[item][key][0]
#		print dish_name[name]

#for item in restaurant:
#	print restaurant[item]

#results = open('key_result.json','w')
#json.dump(result, results)