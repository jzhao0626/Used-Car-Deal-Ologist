import os
from json import loads
from lxml import html
from datetime import datetime
from requests_html import HTMLSession
from .carBrands import carBrands
from .Vehicle import Vehicle


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

def process_raw_vehicle_data(session, tree, city):
    url = tree[0]

    try:
        idpk = int(url.split("/")[-1].strip(".html"))
    except ValueError as e:
        print("{} does not have a valid id: {}".format(url, e), flush=True)
        return None

    new_vehicle = Vehicle(idpk)
    new_vehicle.price = int(tree[1].replace(",", "").strip("$"))

    vehicleDict = {}
    vehicleDict["price"] = int(tree[1].replace(",", "").strip("$"))

    try:
        # grab each individual vehicle page
        page = session.get(url)
        tree = html.fromstring(page.content)
    except:
        print(f"Failed to reach {url}, entry has been dropped", flush=True)
        return None

    new_vehicle = apply_webpage_attributes(new_vehicle, tree.xpath("//span//b"))
	
    # now lets fetch the image url if exists
    try:
        img = tree.xpath('//div[@class="slide first visible"]//img')
        new_vehicle.image_url = img[0].attrib["src"]
    except: pass
    # try to fetch lat/long and city/state, remain as None if they do not exist
    try:
        location = tree.xpath("//div[@id='map']")
        new_vehicle.latitude = float(location[0].attrib["data-latitude"])
        new_vehicle.longitude = float(location[0].attrib["data-longitude"])
    except: pass
	
	# try to fetch a vehicle posting_date
    try:
        new_vehicle.posting_date = tree.xpath(
            "//div[@class='postinginfos']//p[@class='postinginfo reveal']//time"
        )[0].get("datetime")
    except: pass

    new_vehicle.type_convert_data()
    return new_vehicle

def process_vehicle_tree_data(id, price, city, tree):
    # url = tree[0]

    # try:
    #     idpk = int(url.split("/")[-1].strip(".html"))
    # except ValueError as e:
    #     print("{} does not have a valid id: {}".format(url, e), flush=True)
    #     return None

    # new_vehicle = Vehicle(idpk)
    # new_vehicle.price = int(tree[1].replace(",", "").strip("$"))

    # vehicleDict = {}
    # vehicleDict["price"] = int(tree[1].replace(",", "").strip("$"))

    # try:
    #     # grab each individual vehicle page
    #     page = session.get(url)
    #     tree = html.fromstring(page.content)
    # except:
    #     print(f"Failed to reach {url}, entry has been dropped", flush=True)
    #     return None

    new_vehicle = apply_webpage_attributes(new_vehicle, tree.xpath("//span//b"))
	
    # now lets fetch the image url if exists
    try:
        img = tree.xpath('//div[@class="slide first visible"]//img')
        new_vehicle.image_url = img[0].attrib["src"]
    except: pass
    # try to fetch lat/long and city/state, remain as None if they do not exist
    try:
        location = tree.xpath("//div[@id='map']")
        new_vehicle.latitude = float(location[0].attrib["data-latitude"])
        new_vehicle.longitude = float(location[0].attrib["data-longitude"])
    except: pass
	
	# try to fetch a vehicle posting_date
    try:
        new_vehicle.posting_date = tree.xpath(
            "//div[@class='postinginfos']//p[@class='postinginfo reveal']//time"
        )[0].get("datetime")
    except: pass

    new_vehicle.type_convert_data()
    return new_vehicle