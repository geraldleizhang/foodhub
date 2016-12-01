import json
import string
import time
import numpy as np

temp = open('review2analysis.json','r')
reviews = json.load(temp)

ntemp = open('dishname.json','r')
dish_name = json.load(ntemp)

ttemp = open('dishtree.json','r')
dish_tree = json.load(ttemp)



restaurant = {}
restaurant_info = {}
result = {}
author = {}

for item in reviews:
	#print reviews[item][0]['keyword']
	name = reviews[item][0]['restaurant']
	author_name = reviews[item][0]['author']
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

		score = float(review['result']['score'])
		restaurant[name][review['keyword']].append(score)
		author[author_name].append(score)
		#if review['keyword'] == 'salad':
			#print review, score

author_result = {}
author_analysis = np.zeros(20)

for item in author:
	temp = np.array(author[item]).mean()
	ana_temp = int(temp * 10)
	
	#print ana_temp
	author_result[item] = ana_temp
	author_analysis[ana_temp+9] += 1

for item in restaurant:
	result[item] = {}
	for key in restaurant[item]:
		if result[item].has_key(key) == False:
			result[item][key]=0.0
		#print restaurant[item][key]
		temp = np.array(restaurant[item][key])
		score = temp.mean()
		result[item][key] = score

#for i in range(len(author_analysis)):
#	print author_analysis[i]/author_analysis.sum()
#print author_analysis/author_analysis.sum()


print len(dish_tree)
print len(dish_name)
print len(restaurant)

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