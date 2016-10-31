import requests
import bs4
import json
import hashlib

if __name__ == "__main__":
	index_url = "http://www.opentable.com/s/?personalizer=true&covers=2&dateTime=2016-11-01\%2018\%3A30&metroId=16&regionIds=50&pageType=0"
	print index_url
	response = requests.get(index_url)
	urls_soup = bs4.BeautifulSoup(response.text, "html.parser")
	urls_body = urls_soup.body

	urls = urls_body.find_all("a", attrs={"class":"review-link"})
	for item in urls:
		#print item
		#temp = item.find_all("a", attrs={"class":"review-link"})
		#print temp
		print item
		#item = "https://www.tripadvisor.com"+item['href']
		#print item