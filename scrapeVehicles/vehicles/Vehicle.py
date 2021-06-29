from .carBrands import carBrands    

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

class Vehicle:
    """A simple example class"""

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
        print("new car made", flush=True)

    def type_convert_data(self):
        if (self.price):
            try:
                self.price = int(self.price)
            except:
                pass
        if (self.odomoter):
            try:
                self.odomoter = int(self.odomoter)
            except:
                pass
        if (self.model):
            # model actually contains 3 variables that we'd like: year, manufacturer, and model (which we call model)

            # set year
            try:
                self.year = int(self.model[:4])
            except:
                self.year = None
            
            model = self.model[5:]
            foundManufacturer = False
            # we parse through each word in the description and search for a match with carBrands (at the top of the program)
            # if a match is found then we have our manufacturer, otherwise we set model to the entire string and leave manu blank
            for word in model.split():
                if word.lower() in carBrands:
                    foundManufacturer = True
                    model = ""
                    # resolve conflicting manufacturer titles
                    self.manufacturer = fix_manufacturer_errors(manufacturer)
                    continue
                if foundManufacturer:
                    model = model + word.lower() + " "
            self.model = model.strip()
