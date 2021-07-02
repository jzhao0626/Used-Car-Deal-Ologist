from cities.crawlCities import scrapeCitiesAsync as getCities
from vehicles.crawlVehicles import scrapeVehicles as getVehicles
from vehicles.crawlVehiclesAsync import scrape_vehicles_async as scrape_vehicles_async
from lxml import html
from requests_html import HTMLSession
from requests_html import AsyncHTMLSession
import asyncio

def main():
    cities = asyncio.run(getCities())
    asyncio.run(scrape_vehicles_async(cities))
    # create requests session
    # session = HTMLSession()
    # vehicles = getVehicles(session, cities)
    print("done", flush=True)

if __name__ == "__main__":
    main()
