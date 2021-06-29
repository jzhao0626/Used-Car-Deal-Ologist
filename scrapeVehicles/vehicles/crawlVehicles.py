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
    

# def process_raw_vehicles(session, raw_scraped_vehicles):


def scrape_city_pages(session, city):
    page_index = 0
    scraped_vehicles = []

    for i in range(craigslist_page_limit):
        page_url = f"{city.url}/d/cars-trucks/search/cta?s={i * craigslist_vehicles_limit}"
        vehiclesList = scrape_raw_vehicles(session, page_url)
     
        # loop through each vehicle
        for item in vehiclesList:
            url = item[0]
            try:
                idpk = int(url.split("/")[-1].strip(".html"))
            except ValueError as e:
                print("{} does not have a valid id: {}".format(url, e), flush=True)

            new_vehicle = Vehicle(idpk)
            new_vehicle.price = int(item[1].replace(",", "").strip("$"))

            vehicleDict = {}
            vehicleDict["price"] = int(item[1].replace(",", "").strip("$"))

            try:
                # grab each individual vehicle page
                page = session.get(url)
                tree = html.fromstring(page.content)
            except:
                print(f"Failed to reach {url}, entry has been dropped")
                continue


            new_vehicle = apply_webpage_attributes(new_vehicle, tree.xpath("//span//b"))

            # we will assume that each of these variables are None until we hear otherwise
            # that way, try/except clauses can simply pass and leave these values as None
            price = None
            year = None
            manufacturer = None
            model = None
            condition = None
            cylinders = None
            fuel = None
            odometer = None
            title_status = None
            transmission = None
            VIN = None
            drive = None
            size = None
            vehicle_type = None
            paint_color = None
            image_url = None
            lat = None
            long = None
            description = None
            posting_date = None

            # now this code gets redundant. if we picked up a specific attr in the vehicleDict then we can change the variable from None.
            # integer attributes (price/odometer) are handled in case the int() is unsuccessful, but i have never seen that be the case
            if "price" in vehicleDict:
                try:
                    price = int(vehicleDict["price"])
                except Exception as e:
                    print(f"Could not parse price: {e}")
            if "odomoter" in vehicleDict:
                try:
                    odometer = int(vehicleDict["odometer"])
                except Exception as e:
                    print(f"Could not parse odometer: {e}")
            if "condition" in vehicleDict:
                condition = vehicleDict["condition"]
            if "model" in vehicleDict:
                # model actually contains 3 variables that we'd like: year, manufacturer, and model (which we call model)
                try:
                    year = int(vehicleDict["model"][:4])
                    if year > nextYear:
                        year = None
                except:
                    year = None
                model = vehicleDict["model"][5:]
                foundManufacturer = False
                # we parse through each word in the description and search for a match with carBrands (at the top of the program)
                # if a match is found then we have our manufacturer, otherwise we set model to the entire string and leave manu blank
                for word in model.split():
                    if word.lower() in carBrands:
                        foundManufacturer = True
                        model = ""
                        # resolve conflicting manufacturer titles
                        manufacturer = fix_manufacturer_errors(manufacturer)
                        continue
                    if foundManufacturer:
                        model = model + word.lower() + " "
                model = model.strip()
            if "cylinders" in vehicleDict:
                cylinders = vehicleDict["cylinders"]
            if "fuel" in vehicleDict:
                fuel = vehicleDict["fuel"]
            if "odometer" in vehicleDict:
                odometer = vehicleDict["odometer"]
            if "title status" in vehicleDict:
                title_status = vehicleDict["title status"]
            if "transmission" in vehicleDict:
                transmission = vehicleDict["transmission"]
            if "VIN" in vehicleDict:
                VIN = vehicleDict["VIN"]
            if "drive" in vehicleDict:
                drive = vehicleDict["drive"]
            if "size" in vehicleDict:
                size = vehicleDict["size"]
            if "type" in vehicleDict:
                vehicle_type = vehicleDict["type"]
            if "paint color" in vehicleDict:
                paint_color = vehicleDict["paint color"]

            # now lets fetch the image url if exists

            try:
                img = tree.xpath('//div[@class="slide first visible"]//img')
                image_url = img[0].attrib["src"]
            except:
                pass

            # try to fetch lat/long and city/state, remain as None if they do not exist

            try:
                location = tree.xpath("//div[@id='map']")
                lat = float(location[0].attrib["data-latitude"])
                long = float(location[0].attrib["data-longitude"])
            except Exception as e:
                pass

            # try to fetch a vehicle description, remain as None if it does not exist

            try:
                location = tree.xpath("//section[@id='postingbody']")
                # description = location[0].text_content().replace("\n", " ").replace("QR Code Link to This Post", "").strip()
                description = None
            except:
                pass
            try:
                posting_date = tree.xpath(
                    "//div[@class='postinginfos']//p[@class='postinginfo reveal']//time"
                )[0].get("datetime")
            except Exception as e:
                print(e)

            scraped_vehicles.append(new_vehicle)

            # finally we get to insert the entry into the database
            print(
                """INSERT INTO vehicles(id, url, region, region_url, price, year, manufacturer, model, condition,
            cylinders, fuel,odometer, title_status, transmission, VIN, drive, size, type, 
            paint_color, image_url, description, lat, long, state, posting_date)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    idpk,
                    url,
                    city.url,
                    city.state,
                    price,
                    year,
                    manufacturer,
                    model,
                    condition,
                    cylinders,
                    fuel,
                    odometer,
                    title_status,
                    transmission,
                    VIN,
                    drive,
                    size,
                    vehicle_type,
                    paint_color,
                    image_url,
                    description,
                    lat,
                    long,
                    city.name,
                    posting_date,
                ),
            )

            if len(scraped_vehicles) > 99:
                return scraped_vehicles
        
        # these lines will execute every time we grab a new page (after 120 entries)
        print(f"{scraped} vehicles scraped", flush=True)
    
    return scraped_vehicles

def apply_webpage_attributes(vehicle, attributes):
    # this fetches a list of attributes about a given vehicle. each vehicle does not have every specific attribute listed on craigslist
    # so this code gets a little messy as we need to handle errors if a car does not have the attribute we're looking for
    raw_attributes = {}
    for attribute in attributes:
        try:
            # model is the only attribute without a specific tag on craigslist, so if this code fails it means that we've grabbed the model of the vehicle
            tag = attribute.getparent().text.strip()
            tag = tag.strip(":")
        except:
            tag = "model"
        try:
            # # some of these tags are not 100% the same with the vehicle class, have to change them to match
            if tag == "type":
                tag = "car_type"
            if " " in tag:
                tag = tag.replace(" ", "_")
            # this code fails if attribute=None so we have to handle it appropriately
            raw_attributes[tag] = attribute.text.strip()
        except:
            raw_attributes[tag] = None
            pass

    for key, value in raw_attributes.items():
        if (key not in Vehicle.__dict__):
            print(f"could not attach key to class: {key}", flush=True)
        else:
            setattr(vehicle, key, value)

    return vehicle

def fix_manufacturer_errors(manufacturer):
    if manufacturer:
        # resolve conflicting manufacturer titles
        manufacturer = manufacturer.lower()
        if manufacturer == "chev" or manufacturer == "chevy":
            return "chevrolet"
        if manufacturer == "mercedes" or manufacturer == "mercedesbenz":
            return "mercedes-benz"
        if manufacturer == "vw":
            return "volkswagen"
        if manufacturer == "landrover":
            return "land rover"
        if manufacturer == "harley":
            return "harley-davidson"
        if manufacturer == "infinity":
            return "infiniti"
        if manufacturer == "alfa":
            return "alfa-romeo"
        if manufacturer == "aston":
            return "aston-martin"
    return manufacturer


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