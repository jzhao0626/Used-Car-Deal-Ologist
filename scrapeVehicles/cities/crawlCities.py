#crawlCities grabs every city on Craigslist

import re
from lxml import html
from .stateCodes import states

scrape_url_prefix = "https://geo.craigslist.org/iso/us/"

def scrapeState(state, origin, tree):
    scrapedCities = []

    #some states just redirect to a single site, we don't want to leave those out
    if origin.url.split("/")[-1] != state:
        city = tree.xpath("//div[@class='regular-area']//h2[@class='area']")[0].text
        scrapedCities.append((state, city, origin.url))          
    else:
        #cities = list of elements for each region
        cities = tree.xpath('//ul[contains(concat( " " , @class, " "), " geo-site-list ")]//li//a')
        
        #major cities are presented in bold text, this must be handled
        boldAt = 0
        for item in cities:
            city = item.text
            #if city == None, text is in bold
            if city == None:
                city = item.xpath("//b")[boldAt].text
                boldAt += 1
            if not re.match(r"[a-z]*, [A-Z]*", city):
                #insert url and city city, easy stuff
                city = city.replace("'", "''")
                link = item.attrib['href']
                #there are some suburbs of cities in different states with weird cars+trucks / housing links, ignore those.
                if link[:4] != "http":
                    continue
                scrapedCities.append((state, city, link))  

    return scrapedCities

def scrapeCities(session):
    cities = []
    for state in states:
        origin = session.get(scrape_url_prefix + state)
        tree = (html.fromstring(origin.content))       
        new_cities = scrapeState(state, origin, tree)
        if (len(new_cities) > 0):
            cities = cities + new_cities

    return cities