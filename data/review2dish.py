import json
import string

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
dish_name = []
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
			dish_name.append(i)



dish_key_temp = sorted(dish_key_temp.items(), lambda x, y: cmp(x[1], y[1]))
for item in dish_key_temp:
	#print item[1]
	if item[1] > 4 and len(item[0])>2:
		dish_key.append(item[0]) 

#for item in dish_key:
#	print item

for item in dish_name:
	sig = 0
	for key in dish_key:
		if item.find(key) != -1:
			sig = 1
			continue
	if sig==0:
		#print item
		dish_name.remove(item)

for item in dish_name:
	print item

#get useful reviews
num=0
print len(reviews)
for item in reviews:
	temp = item['review'].encode('utf8')
	signal = 0
	for dish in dish_name:
		if temp.find(dish) != -1:
			if len(dish) > 10:
				print dish
			signal = 1
	if signal == 1:
		num += 1
	#print temp
print num




#for item in reviews:
#	temp = item['review'].split(".")
#	for i in temp:
#		if i == "":
#			continue
#		if i.strip().lower().find('sticky')!=-1:
#			print i.strip().lower()
#	#break
	