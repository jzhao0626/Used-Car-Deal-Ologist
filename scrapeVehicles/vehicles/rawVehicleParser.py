import os
from json import loads
from lxml import html
from datetime import datetime
from requests_html import HTMLSession
from .carBrands import carBrands
from .Vehicle import Vehicle

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

def process_raw_vehicle_data(session, raw_data):
    url = raw_data[0]

    try:
        idpk = int(url.split("/")[-1].strip(".html"))
    except ValueError as e:
        print("{} does not have a valid id: {}".format(url, e), flush=True)
        return None

    new_vehicle = Vehicle(idpk)
    new_vehicle.price = int(raw_data[1].replace(",", "").strip("$"))

    vehicleDict = {}
    vehicleDict["price"] = int(raw_data[1].replace(",", "").strip("$"))

    try:
        # grab each individual vehicle page
        page = session.get(url)
        tree = html.fromstring(page.content)
    except:
        print(f"Failed to reach {url}, entry has been dropped", flush=True)
        return None

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
        new_vehicle.image_url = img[0].attrib["src"]
    except:
        pass

    # try to fetch lat/long and city/state, remain as None if they do not exist
    try:
        location = tree.xpath("//div[@id='map']")
        new_vehicle.latitude = float(location[0].attrib["data-latitude"])
        new_vehicle.longitude = float(location[0].attrib["data-longitude"])
    except:
        pass

    # try to fetch a vehicle description
    try:
        new_vehicle.location = tree.xpath("//section[@id='postingbody']")
        new_vehicle.description = location[0].text_content().replace("\n", " ").replace("QR Code Link to This Post", "").strip()
    except:
        pass
	
	# try to fetch a vehicle posting_date
    try:
        new_vehicle.posting_date = tree.xpath(
            "//div[@class='postinginfos']//p[@class='postinginfo reveal']//time"
        )[0].get("datetime")
    except:
        pass
    
    print(new_vehicle.__dict__, flush=True)
    # print(vehicleDict, flush=True)
    # print(price, year, manufacturer, model, condition, cylinders, fuel, odometer, title_status, transmission, VIN, drive, size, vehicle_type, paint_color, image_url, lat, long, description, posting_date, flush=True)
    return new_vehicle