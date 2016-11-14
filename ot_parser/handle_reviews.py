import json

dish = {}

rtemp = open('reviews.json','r')
reviews = json.load(rtemp)

mtemp = open('restaurant.json','r')
restaurant = json.load(mtemp)

mmtemp = open('ta_restaurant.json','r')
rt = json.load(mmtemp)

#for item in rt:
restaurant.extend(rt)
print restaurant

for item in restaurant:
	#print item['name']
	if item['menu'] == []:
		continue
	temp = item['menu']
	if temp == None:
		continue
	for i in temp:
		#if i.lower().find('roll') != -1:
		#	print item['name'], i
		for t in i.split(' '):
			tt = t.lower()
			if tt[0].isalpha() == False:
				continue
			if dish.has_key(tt) == True:
				dish[tt] += 1
			else:
				dish[tt] = 1


dish = sorted(dish.items(), lambda x, y: cmp(x[1], y[1]))
print dish

#for item in reviews:
#	temp = item['review'].split(".")
#	for i in temp:
#		if i == "":
#			continue
#		if i.strip().lower().find('sticky')!=-1:
#			print i.strip().lower()
#	#break
	