import json
import string
import time

#loading all data
otemp = open('ot_reviews.json','r')
reviews = json.load(otemp)

ttemp = open('ta_reviews.json','r')
reviews.extend(json.load(ttemp))

ytemp = open('ye_reviews.json','r')
reviews.extend(json.load(ytemp))


otemp = open('ot_restaurant.json','r')
restaurant = json.load(otemp)

ttemp = open('ta_restaurant.json','r')
restaurant.extend(json.load(ttemp))

ytemp = open('ye_restaurant.json','r')
restaurant.extend(json.load(ytemp))


#get common dish name keyword list
dish_key_temp = {}
dish_key = []
dish_name = {}
#build dish_key -> dish_name
dish_key_namelist = {}
dish_key_related = {}
dish_name_key = {}
for item in restaurant:
	#print item['name']
	if item['menu'] == []:
		continue
	temp = item['menu']
	if temp == None:
		continue
	for i in temp:
		i = i.encode('utf8').translate(None, string.punctuation).lower()
		hasdish=0
		for t in i.split(' '):
			#t=t.encode('utf8')
			#tt = t.translate(None, string.punctuation).lower()
			if t == "":
				continue
			if t[0].isalpha() == False:
				continue
			if dish_key_temp.has_key(t) == True:
				dish_key_temp[t] += 1
				hasdish = 1
			else:
				dish_key_temp[t] = 1
				hasdish = 1
		if hasdish == 1:
			#dish_name.append(i)
			if dish_name.has_key(i):
				dish_name[i].append(item['name'].encode('utf8'))
			else:
				dish_name[i]=[]
				dish_name[i].append(item['name'].encode('utf8'))



#dish_key_temp = sorted(dish_key_temp.items(), lambda x, y: cmp(x[1], y[1]))
for item in dish_key_temp:
	if dish_key_temp[item] > 4 and len(item)>2:
		dish_key.append(item) 
		dish_key_namelist[item] = []
		dish_key_related[item] = {}
#print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
for item in dish_name.keys():
#	print item
	sig = 0
	key_temp = []
	dish_name_key[item]=[]
	for key in dish_key:
		if item.find(key) != -1:
			sig = 1
			key_temp.append(key)
			dish_key_namelist[key].append(item)
			dish_name_key[item].append(key)
			#continue
	if sig==0:
		#print item
		dish_name.pop(item)
		dish_name_key.pop(item)
		continue
	for key in key_temp:
		for t in key_temp:
			if t != key:
				if dish_key_related[key].has_key(t) == True:
					dish_key_related[key][t] += 1
				else:
					dish_key_related[key][t] = 1
				#dish_key_related[key].append(t)

#for item in dish_key:
#	print item
#for item in dish_key_namelist:
#	print item, len(dish_key_namelist[item])
#for item in dish_key_related:
#	dish_key_related[item] = sorted(dish_key_related[item].items(), lambda x, y: cmp(x[1], y[1]))
#	print item, dish_key_related[item]

#key-key-dish
dish_name_tree = {}


for root in dish_key_related:
	dish_name_tree[root]={}
	for leaf in dish_key_related[root]:
		dish_name_tree[root][leaf]=[]
		for dish in dish_name_key:
			if dish_name_key[dish].count(root) and dish_name_key[dish].count(leaf):
				dish_name_tree[root][leaf].append(dish)
		if dish_name_tree[root][leaf]==[]:
			dish_name_tree[root].pop(leaf)

for item in dish_name_tree:
	if dish_name_tree[item]=={}:
		continue
	print item, dish_name_tree[item]
	#for temp in dish_name_tree[item]:
	#	print dish_name_tree[item][temp] 
print "done"

time.sleep(100)



num = 0
for item in dish_name:
	dish_name[item] = list(set(dish_name[item]))
	#print item, dish_name[item]
	if len(dish_name[item]) > 1:
		num += 1
		print item, dish_name[item], len(dish_name[item])
print num
print len(dish_name)

#get useful reviews
dish_name_reviews = {}
num=0
useful_reviews=[]
#print len(reviews)
for item in reviews:
	temp = item['review'].encode('utf8').split(".")
	signal = 0
	for dish in dish_name:
		for sentence in temp:
			if sentence.find(dish) != -1:
				#if len(dish) > 10:
				#	print dish
				signal = 1
				data = {
					'restaurant' : item['restaurant'],
                	'time' : item['time'],
                	'author' : item['author'],
                	'review' : sentence,
                	'point' : 0.0,
                	'keyword' : dish_name_key[dish]      	
				}
				if dish_name_reviews.has_key(dish):
					dish_name_reviews[dish].append(data)
				else:
					dish_name_reviews[dish] = []
					dish_name_reviews[dish].append(data)
	if signal == 1:
		num += 1
		#useful_reviews.append(temp)
	#print temp
print num

review2dish = open('review2dish.json','w')
json.dump(dish_name_reviews, review2dish)

#for item in useful_reviews:
#	print item
num = 0
for item in dish_name_reviews:
	if len(dish_name_reviews[item]) > 3:
		print item,  dish_name_reviews[item], len(dish_name_reviews[item])
		num += 1
print num






#for item in reviews:
#	temp = item['review'].split(".")
#	for i in temp:
#		if i == "":
#			continue
#		if i.strip().lower().find('sticky')!=-1:
#			print i.strip().lower()
#	#break
	