# scrapeVehicles.py loops through all cities listed on Craigslist and scrapes every vehicle for sale and adds it to cities.db
# this program will take awhile to run, don't run unless you're willing to let it sit for at least 2 hours
# the database is commited after we've finished scraping each city, so the program can be terminated and results are still saved if you need to exit for any reason

import os
from json import loads
from lxml import html
from datetime import datetime
from requests_html import HTMLSession
from .carBrands import carBrands
from .Vehicle import Vehicle
from .rawVehicleParser import process_raw_vehicle_data

# each city contains max 3_000 entries
craigslist_page_limit = 25
# each search page contains 120 entries
craigslist_vehicles_limit = 120

def scrape_raw_vehicles(session, page_url):
    try:
        page = session.get(page_url)
    except Exception as e:
        # catch any excpetion and continue the loop if we cannot access a site for whatever reason
        print(f"Failed to reach {page_url}, entries have been dropped: {e}")
        return None

    tree = html.fromstring(page.content)

    # the following line returns a list of urls for different vehicles
    vehicles = tree.xpath('//a[@class="result-image gallery"]')

    if len(vehicles) == 0:
        return None

    raw_vehicles = []

    for item in vehicles:
        vehicleDetails = []
        vehicleDetails.append(item.attrib["href"])
        try:
            # this code attempts to grab the price of the vehicle. some vehicles dont have prices (which throws an exception)
            # and we dont want those which is why we toss them
            vehicleDetails.append(item[0].text)
        except:
            continue
        raw_vehicles.append(vehicleDetails)

    return raw_vehicles


def scrape_city_pages(session, city):
    page_index = 0
    scraped_vehicles = []

    for i in range(craigslist_page_limit):
        page_url = f"{city.url}/d/cars-trucks/search/cta?s={i * craigslist_vehicles_limit}"
        vehiclesList = scrape_raw_vehicles(session, page_url)

        for raw_vehicle in vehiclesList:
            new_vehicle = process_raw_vehicle_data(session, raw_vehicle)
            
            if (new_vehicle != None):
                scraped_vehicles.append(new_vehicle)
        
            if len(scraped_vehicles) > 99:
                return scraped_vehicles

        # these lines will execute every time we grab a new page (after 120 entries)
        print(f"{len(scraped_vehicles)} vehicles scraped", flush=True)
    
    return scraped_vehicles


def scrapeVehicles(cities):
    scraped_vehicles = []
    session = HTMLSession()

    # if the car year is beyond next year, we toss it out. this variable is used later
    nextYear = datetime.now().year + 1

    cities_count = len(cities)
    for i in range(cities_count):
        new_vehicles = scrape_city_pages(session, cities[i])
        if (len(new_vehicles) > 0):
            scraped_vehicles = scraped_vehicles + new_vehicles
            return scraped_vehicles