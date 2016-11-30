import json
import string
import time

temp = open('review2analysis.json','r')
reviews = json.load(temp)

ntemp = open('dishname.json','r')
dish_name = json.load(ntemp)

ttemp = open('dishtree.json','r')
dish_tree = json.load(ttemp)



restaurant = {}
restaurant_info = {}


for item in reviews:
	name = reviews[item][0]['restaurant']
	print reviews[item][0]
	if restaurant.has_key(name):
		restaurant[name][item] = {}
	else:
		restaurant[name] = {}
		restaurant[name][item] = {}
	
	#restaurant[reviews[item][0]['restaurant']]
	score = 0.0
	for review in reviews[item]:
		score += float(review['result']['score'])
		
	#print item, len(reviews[item]), score / len(reviews[item])
	restaurant[name][item] = score / len(reviews[item])
#for item in dish_tree:
#	for key in dish_tree[item]:
#		name = dish_tree[item][key][0]
#		print dish_name[name]

#for item in restaurant:
#	print restaurant[item]

result = open('simple_result.json','w')
json.dump(restaurant, result)