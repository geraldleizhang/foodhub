import requests
import bs4
import json
import hashlib
#from html.parser import HTMLParser

restaurant_file = 'restaurant.json'
reviews_file = 'reviews.json'
#menu_file = 'menu.json'
restaurant_data = []
reviews_data = []
#menu_data = []
index_urls = []



def parser_restaurantFeature(index_url):
    response = requests.get(index_url)
    print index_url
    business_soup = bs4.BeautifulSoup(response.text, "html.parser")
    business_body = business_soup.body
    
    business_name = business_soup.title.text
    business_name = business_name[:business_name.find("Restaurant")-1]
    #business_name = business_media_wrapper.text.strip()
    #print "name is "
    #print business_name

    business_address_wrapper = business_soup.find_all("meta", attrs={"property":"business:contact_data:street_address"})
    #print business_address
    business_address = business_address_wrapper[0]['content']
    business_address_wrapper = business_soup.find_all("meta", attrs={"itemprop":"postalCode"})
    business_address = business_address + " , " + business_address_wrapper[0]['content']
    #print "address is "
    #print business_address

    
    menus_wrapper = business_body.find_all("div", attrs={"class": "rest-menu-item-title"})
    menus=[]
    for menu_wrapper in menus_wrapper:
        #print menu_wrapper.text
        menus.append(menu_wrapper.text)

    data = {
            #'business_id' : business_id,
            'name' : business_name ,
            'full_address' : business_address, 
            'menu' : menus
            }
    
    restaurant_data.append(data)
    return data

def parser_brs(brs):
    review = ""
    review_brs = brs
    while review_brs is not None:
        if isinstance(review_brs.contents[0] , basestring):
            review += review_brs.contents[0]
        review_brs = review_brs.br
    return review

def parser_reviews(index_url):
    response = requests.get(index_url)
    reviews_soup = bs4.BeautifulSoup(response.text, "html.parser")
    reviews_body = reviews_soup.body

    business_name = reviews_soup.title.text
    business_name = business_name[:business_name.find("Restaurant")-1]
    #print "name is "
    #print business_name

    review_urls = []
    review_urls.append(index_url)
    for i in range(2,10):
        review_url = index_url + "&page=" + str(i)
        #print review_url.strip()
        review_urls.append(review_url.strip())

    #business_id_wrapper = reviews_body.find("div", attrs={"class": "lightbox-map hidden"})
    #business_id = business_id_wrapper['data-business-id']
    for item in review_urls:
        #print item
        response = requests.get(item)
        reviews_soup = bs4.BeautifulSoup(response.text, "html.parser")
        reviews_body = reviews_soup.body
        reviews_wrapper = reviews_soup.find_all("div", attrs={"itemprop": "review"})
        #print reviews_wrapper
        for review_wrapper in reviews_wrapper:
            #print temp
            author = review_wrapper.find("span", attrs={"itemprop": "name"})
            author = author.text
            #print "author is"
            #print author.text.strip()
            time = review_wrapper.find("meta", attrs={"itemprop": "datePublished"})
            #print "time is", time
            time =  time['content']

            review = review_wrapper.find("div", attrs={"itemprop": "reviewBody"})
            #print "review is"
            review = review.text.strip()
            #print review

            data = {
                'restaurant' : business_name,
                'time' : time,
                'author' : author,
                'review' : review
            }
            reviews_data.append(data)
    
    return data


def parser_menu(index_url):
    menu_url = index_url
    #print menu_url
    menu_response = requests.get(menu_url)
    menu_soup = bs4.BeautifulSoup(menu_response.text, "html.parser")
    if "Menu" not in menu_soup.title.string:
        return
    menu_body = menu_soup.body

    menus_wrapper = menu_soup.find_all("div", attrs={"class": "rest-menu-item-title"})
    menus = []

    for menu_wrapper in menus_wrapper:
        print menu_wrapper.text
        menus.append(menu_wrapper.text)
    return menus


if __name__ == "__main__":
    #index_urls.append('http://www.yelp.com/biz/aviva-by-kameel-atlanta')
    #index_urls.append('http://www.yelp.com/biz/%C3%A9br%C3%ACk-coffee-room-atlanta')
    #index_urls.append('http://www.yelp.com/biz/jenis-splendid-ice-creams-atlanta')
    
        #TODO: Lei Zhang
        #index_urls = Function get urls
    #urls = open("urls.txt")
    urls = open("urls.txt")
    while 1:
        line = urls.readline()
        if not line:
            break
        index_urls.append(line)

    for index_url in index_urls:
        parser_restaurantFeature(index_url)
        parser_reviews(index_url)
        #parser_menu(index_url)

    businessFile = open(restaurant_file, 'w')
    json.dump(restaurant_data, businessFile)

    reviewsFile = open(reviews_file, 'w')
    json.dump(reviews_data, reviewsFile)

    #menuFile = open(menu_file, 'w')
    #json.dump(menu_data, menuFile)
        
