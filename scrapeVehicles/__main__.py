from cities.crawlCities import scrapeCities as getCities
from vehicles.crawlVehicles import scrapeVehicles as getVehicles
from lxml import html
from requests_html import HTMLSession


def main():
    # create requests session
    session = HTMLSession()
    cities = getCities(session)
    for city in cities:
        print(city)
    print("inside module", flush=True)
    vehicles = getVehicles(cities)
    print("done", flush=True)


if __name__ == "__main__":
    main()
