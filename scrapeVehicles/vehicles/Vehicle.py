from .carBrands import carBrands 

class Vehicle:

    id = None
    url = None
    region = None
    region_url = None
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
    car_type = None
    paint_color = None
    image_url = None
    description = None
    latitude = None
    longitude = None
    state = None
    posting_date = None

    def __init__(self, id):
        self.id = id

    def __str__(self):
        return f"{self.__dict__}"

    def type_convert_data(self):
        if (self.cylinders):
            if ("cylinders" in self.cylinders):
                self.cylinders = self.cylinders.replace("cylinders", "").strip()
        if (self.price):
            try: self.price = int(self.price)
            except: pass
        if (self.odometer):
            try: self.odometer = int(self.odometer)
            except: pass
        #model actually contains 3 variables that we'd like: year, manufacturer, and model (which we call model)
        if (self.model):
            try: self.year = int(self.model[:4])
            except: self.year = None
            self.model = self.model[5:]
            foundManufacturer = False
            #we parse through each word in the description and search for a match with carBrands (at the top of the program)
            #if a match is found then we have our manufacturer, otherwise we set model to the entire string and leave manu blank
            for word in self.model.split():
                if word.lower() in carBrands:
                    foundManufacturer = True
                    self.model = ""
                    #resolve conflicting manufacturer titles
                    manufacturer = word.lower()
                    if manufacturer == "chev" or manufacturer == "chevy":
                        self.manufacturer = "chevrolet"
                    elif manufacturer == "mercedes" or manufacturer == "mercedesbenz":
                        self.manufacturer = "mercedes-benz"
                    elif manufacturer == "vw":
                        self.manufacturer = "volkswagen"
                    elif manufacturer == "landrover":
                        self.manufacturer = "land rover"
                    elif manufacturer == "harley":
                        self.manufacturer = "harley-davidson"
                    elif manufacturer == "infinity":
                        self.manufacturer = "infiniti"
                    elif manufacturer == "alfa":
                        self.manufacturer = "alfa-romeo"
                    elif manufacturer == "aston":
                        self.manufacturer = "aston-martin"
                    else:
                        self.manufacturer = manufacturer
                    continue
                if foundManufacturer:
                    self.model = self.model + word.lower() + " "
                    
            self.model = self.model.strip()





vehicle_condition_map = {
    "new": 1,
    "like new": 2,
    "excellent": 3,
    "good": 4,
    "fair": 5,
    "salvage": 6,
}

vehicle_size_map = {
    "compact": 1,
    "sub-compact": 2,
    "mid-size": 3,
    "full-size": 4,
}