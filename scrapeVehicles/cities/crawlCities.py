# crawlCities grabs every name on Craigslist

import re
from lxml import html
from .stateCodes import states
from .City import City
from requests_html import AsyncHTMLSession
import asyncio

scrape_url_prefix = "https://geo.craigslist.org/iso/us/"


def scrapeState(origin, tree, state):
    scrapedCities = []

    # some states just redirect to a single site, we don't want to leave those out
    if origin.url.split("/")[-1] != state:
        name = tree.xpath("//div[@class='regular-area']//h2[@class='area']")[0].text
        scrapedCities.append(City(name=name, state=state, url=origin.url))
    else:
        # cities = list of elements for each region
        cities = tree.xpath(
            '//ul[contains(concat( " " , @class, " "), " geo-site-list ")]//li//a'
        )

        # major cities are presented in bold text, this must be handled
        boldAt = 0
        for item in cities:
            name = item.text
            # if name == None, text is in bold
            if name == None:
                name = item.xpath("//b")[boldAt].text
                boldAt += 1
            if not re.match(r"[a-z]*, [A-Z]*", name):
                # insert name, state, and name; easy stuff
                name = name.replace("'", "''")
                link = item.attrib["href"]
                # there are some suburbs of cities in different states with weird cars+trucks / housing links, ignore those.
                if link[:4] != "http":
                    continue
                scrapedCities.append(City(name=name, state=state, url=link))

    return scrapedCities


async def scrapeStateForCitiesAsync(session, base_url, state):
    page = await session.get(base_url + state)
    tree = html.fromstring(page.content)
    new_cities = scrapeState(page, tree, state)
    new_cities_count = len(new_cities) if new_cities is not None else 0
    if new_cities_count > 0:
        return new_cities
    else:
        return []


async def scrapeCitiesAsync():
    cities = []
    session = AsyncHTMLSession()
    tasks = (
        scrapeStateForCitiesAsync(session, scrape_url_prefix, state) for state in states
    )
    citiesLists = await asyncio.gather(*tasks)
    for citiesList in citiesLists:
        if len(citiesList) > 0:
            cities = cities + citiesList
    return cities
