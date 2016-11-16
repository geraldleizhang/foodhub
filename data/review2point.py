import json
from watson_developer_cloud import AlchemyLanguageV1
from alchemyapi import AlchemyAPI

#alchemy_language = AlchemyLanguageV1(api_key='d0e3063c3b5525d7f1adcac84acc26117ca59bfb')

#temp = open('review2dish.json','r')
#analysis_temp = open('review2analysis.json','w')
#reviews = json.load(temp)
#result=[]
#for item in reviews:
#	print reviews[item][0]['point']
#	print item, reviews[item][0]['keyword'], reviews[item][0]['review']
#	response = alchemy_language.targeted_sentiment(text=reviews[item][0]['review'], targets=reviews[item][0]['keyword'])
#	print response
#	result.append(response)
#	break
#json.dump(result, analysis_temp)
	
alchemyapi = AlchemyAPI()
#alchemy_language = AlchemyLanguageV1(api_key='d0e3063c3b5525d7f1adcac84acc26117ca59bfb')


temp = open('review2dish.json','r')
analysis_temp = open('review2analysis.json','w')
reviews = json.load(temp)
results={}
for item in reviews:
	#print reviews[item][0]['review']
	for t in reviews[item][0]['keyword']:
		#print t.encode('utf8') 
	#print reviews[item][0]['keyword']
	#print item, reviews[item][0]['keyword'][0].encode('utf8'), reviews[item][0]['review']
		response = alchemyapi.sentiment_targeted('text', reviews[item][0]['review'], t.encode('utf8') )
	#(text=reviews[item][0]['review'], targets=reviews[item][0]['keyword'])
		print response['status']
		if response['status'] == 'OK':
			ana_result={
				'keyword': t.encode('utf8'),
				'review' : reviews[item][0]['review'],
				'result' : response['docSentiment']
			}
			if results.has_key(item):
				results[item].append(ana_result)
			else:
				results[item] = []
				results[item].append(ana_result)
	#result.append(response)
	#break
json.dump(results, analysis_temp)



#response = alchemyapi.sentiment_targeted('text', demo_text, 'Denver')


#print(json.dumps(
#  alchemy_language.targeted_sentiment(
#    url='http://www.zacks.com/stock/news/207968/stock-market-news-for-february-19-2016',
#    text='fdsiojsdoifjo',
#    targets=['NASDAQ', 'Dow']),
#  indent=2))
