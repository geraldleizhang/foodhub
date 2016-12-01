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

for item in reviews:
	#print reviews[item][0]['keyword']
	name = reviews[item][0]['restaurant']
	#print reviews[item][0]
	if restaurant.has_key(name) == False:
		restaurant[name] = {}
	
	
	#restaurant[reviews[item][0]['restaurant']]
	#score = 0.0
	for review in reviews[item]:
		#print name, review['keyword'], review['result']['score']
		if restaurant[name].has_key(review['keyword']) == False:
			restaurant[name][review['keyword']] = []
		score = float(review['result']['score'])
		restaurant[name][review['keyword']].append(score)

for item in restaurant:
	result[item] = {}
	for key in restaurant[item]:
		if result[item].has_key(key) == False:
			result[item][key]=0.0
		#print restaurant[item][key]
		temp = np.array(restaurant[item][key])
		score = temp.mean()
		result[item][key] = score

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

results = open('key_result.json','w')
json.dump(result, results)