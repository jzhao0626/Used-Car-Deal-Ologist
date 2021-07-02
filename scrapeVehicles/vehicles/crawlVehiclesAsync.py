# scrapeVehicles.py loops through all cities listed on Craigslist and scrapes every vehicle for sale and adds it to cities.db
# this program will take awhile to run, don't run unless you're willing to let it sit for at least 2 hours
# the database is commited after we've finished scraping each city, so the program can be terminated and results are still saved if you need to exit for any reason

import os
from json import loads
from lxml import html
from datetime import datetime
from requests_html import AsyncHTMLSession
import asyncio
from .Vehicle import Vehicle
from .rawVehicleParser import process_vehicle_tree_data

debug_mode = True
# each city contains max 3_000 entries
craigslist_page_limit = 25
# each search page contains 120 entries
craigslist_vehicles_limit = 120


async def scrape_raw_vehicle_async(session, city, tree):
    url = tree[0]
    idpk = None
    price = None
    try:
        idpk = int(url.split("/")[-1].strip(".html"))
        price = int(tree[1].replace(",", "").strip("$"))
    except ValueError as e:
        return None

    print(f"Found {idpk} for price {price}", flush=True)
    vehicle = Vehicle(idpk)
    vehicle.price = price
    return vehicle
    # new_vehicle = process_vehicle_tree_data(session, city, tree)
    # if new_vehicle:
    #     scraped_vehicles.append(new_vehicle)

async def scrape_city_vehicles_pages_async(session, city):
    vehicles_pages = []

    for i in range(craigslist_page_limit):
        page_url = (
            f"{city.url}/d/cars-trucks/search/cta?s={i * craigslist_vehicles_limit}"
        )

        try:
            page = await session.get(page_url)
        except Exception as e:
            # catch any excpetion and continue the loop if we cannot access a site for whatever reason
            break

        tree = html.fromstring(page.content)
        # the following line returns a list of urls for different vehicles
        vehicles = tree.xpath('//a[@class="result-image gallery"]')
        vehicles_count = len(vehicles) if vehicles is not None else 0
        if vehicles_count < 1:
            break

        vehicles_pages = vehicles_pages + vehicles

        # debug
        if (debug_mode):
            break

    pages_count = len(vehicles_pages) if vehicles_pages is not None else 0
    print(f"{pages_count} vehicles pages scraped for {city}", flush=True)

    if pages_count > 0:
        return (city, vehicles_pages)
    else:
        return (city, [])


async def scrape_vehicles_async(cities):
    if (debug_mode):
        cities = cities[:5]

    session = AsyncHTMLSession()
    find_vehicles_pages = (
        scrape_city_vehicles_pages_async(session, city) for city in cities
    )
    vehicles_pages = await asyncio.gather(*find_vehicles_pages)
    if len(vehicles_pages) < 1:
        return
    
    # clean the pages
    cities_n_vehicles_pages = [page for page in vehicles_pages if len(vehicles_pages[1]) > 0]
    print(f"cities_n_vehicles_pages len {len(cities_n_vehicles_pages)}", flush=True)

    # create a list of vehicle and state pairs
    city_n_vehicles = []
    for city_n_vehicles_pages in cities_n_vehicles_pages:
        vehicles_pages = [vehicle for  vehicle in city_n_vehicles_pages[1]]
        for vehicle in vehicles_pages:
            city_n_vehicles.append((city_n_vehicles_pages[0], vehicle))
    print(f"city_n_vehicle len {len(city_n_vehicles)}", flush=True)

    # find_vehicles = (
    #     scrape_raw_vehicle_async(session, city_n_vehicle[0], city_n_vehicle[1]) for city_n_vehicle in city_n_vehicles
    # )
    # vehicles = await asyncio.gather(*find_vehicles)
    # # clean the null vehicles
    # vehicles = [vehicle for vehicle in vehicles if vehicle]
    # print(f"vehicles len {len(vehicles)}", flush=True)
    
