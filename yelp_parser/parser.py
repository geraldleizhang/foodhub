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
    business_soup = bs4.BeautifulSoup(response.text, "html.parser")
    business_body = business_soup.body
    business_id_wrapper = business_body.find("div", attrs={"class": "lightbox-map hidden"})
    business_id = business_id_wrapper['data-business-id']
    
    business_media_wrapper = business_body.find("div", attrs={"class": "media-story"})
    business_name_wrapper = business_media_wrapper.find("a")
    business_name_span = business_name_wrapper.contents[0]
    business_name = business_name_span.contents[0]
    
    business_address_wrapper = business_media_wrapper.find("address")
    business_address = business_address_wrapper.contents[0]
    business_address = business_address.strip()

    menu = parser_menu(index_url, business_id)

    data = {
            #'business_id' : business_id,
            'name' : business_name ,
            'full_address' : business_address, 
            'menu' : menu
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

    business_media_wrapper = reviews_body.find("div", attrs={"class": "media-story"})
    business_name_wrapper = business_media_wrapper.find("a")
    business_name_span = business_name_wrapper.contents[0]
    business_name = business_name_span.contents[0]


    #business_id_wrapper = reviews_body.find("div", attrs={"class": "lightbox-map hidden"})
    #business_id = business_id_wrapper['data-business-id']
    temps_wrapper = reviews_body.find_all("div", attrs={"itemprop": "review"})
    for temp in temps_wrapper:
        time = temp.find("meta", attrs={"itemprop" : "datePublished"})
        print time


    reviews_wrapper = reviews_body.find_all("p", attrs={"itemprop": "description"})
    reviews = []

    for review_wrapper in reviews_wrapper:
        review = ""
        review_contents = review_wrapper.contents
        review += review_contents[0]
        
        review_brs = review_wrapper.br
        if review_brs is not None:
            review += parser_brs(review_brs)
        reviews.append(review)
        review_copy = review
        review_id = hashlib.sha224(review_copy.encode('utf-8')).hexdigest()
        data = {
            'review_id' : review_id,
            #'business_id' : business_id,
            'name' : business_name,
            'text' : review
            }
        reviews_data.append(data)
    
    return data


def parser_menu(index_url, business_id):
    menu_url = index_url.replace('biz','menu')
    print menu_url
    menu_response = requests.get(menu_url)
    menu_soup = bs4.BeautifulSoup(menu_response.text, "html.parser")
    if "Menu" not in menu_soup.title.string:
        return
    menu_body = menu_soup.body

    menus_wrapper = menu_body.find_all("div", attrs={"class": "menu-item-details"})
    menus = []

    for menu_wrapper in menus_wrapper:
        menu_name = menu_wrapper.find("h4")
        if menu_name.find("a") is not None:
            menus.append(menu_name.find("a").string.encode("utf-8"))
            #data = {
            #'business_id' : business_id,
            #'menu' : menu_name.find("a").string
            #}
            #menu_data.append(data)
    
    #data = {
    #        'business_id' : business_id,
    #        'menu' : menus
    #        }
    #menu_data.append(data)
    return menus


if __name__ == "__main__":
    #index_urls.append('http://www.yelp.com/biz/aviva-by-kameel-atlanta')
    #index_urls.append('http://www.yelp.com/biz/%C3%A9br%C3%ACk-coffee-room-atlanta')
    #index_urls.append('http://www.yelp.com/biz/jenis-splendid-ice-creams-atlanta')
    
        #TODO: Lei Zhang
        #index_urls = Function get urls
    #urls = open("urls.txt")
    urls = open("test.txt")
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
        
