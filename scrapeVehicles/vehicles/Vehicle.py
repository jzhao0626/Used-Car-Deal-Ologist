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
