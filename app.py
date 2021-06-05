from flask import Flask, render_template, redirect, current_app as app
from mapping_values import vehicle_condition_map, vehicle_size_map
from Load_SVR import submit_model

error_text = "PLEASE FILL OUT ALL THE DATA"

color = [
    "Color",
    "blue",
    "white",
    "grey",
    "black",
    "brown",
    "red",
    "silver",
    "green",
    "yellow",
    "purple",
    "custom",
    "orange",
]
condition = [
    "Condition",
    "new",
    "like new",
    "excellent",
    "good",
    "fair",
    "salvage",
]
cyl = ["Drive", "Front Wheel Drive", "Rear Wheel Drive", "Four Wheel Drive"]
fuel_type = [
    "Fuel_Type",
    "electric",
    "hybrid",
    "gas",
    "diesel",
    "other",
]
manufacturer = [
    "Make",
    "bmw",
    "toyota",
    "honda",
    "chevrolet",
    "mazda",
    "ford",
    "volvo",
    "cadillac",
    "saturn",
    "subaru",
    "dodge",
    "gmc",
    "ram",
    "chrysler",
    "mercedes-benz",
    "infiniti",
    "jeep",
    "buick",
    "nissan",
    "volkswagen",
    "mercury",
    "hyundai",
    "lexus",
    "porsche",
    "rover",
    "audi",
    "fiat",
    "mini",
    "mitsubishi",
    "lincoln",
    "jaguar",
    "kia",
    "pontiac",
    "acura",
    "tesla",
    "alfa-romeo",
    "datsun",
    "harley-davidson",
    "land rover",
    "aston-martin",
    "ferrari",
]
odometer = "Odometer"
size = [
    "Vehicle_Size",
    "compact",
    "sub-compact",
    "mid-size",
    "full-size",
]
state = [
    "State",
    "al",
    "ak",
    "az",
    "ar",
    "ca",
    "co",
    "ct",
    "dc",
    "de",
    "fl",
    "ga",
    "hi",
    "id",
    "il",
    "in",
    "ia",
    "ks",
    "ky",
    "la",
    "me",
    "md",
    "ma",
    "mi",
    "mn",
    "ms",
    "mo",
    "mt",
    "nc",
    "ne",
    "nv",
    "nj",
    "nm",
    "ny",
    "nh",
    "nd",
    "oh",
    "ok",
    "or",
    "pa",
    "ri",
    "sc",
    "sd",
    "tn",
    "tx",
    "ut",
    "vt",
    "va",
    "wa",
    "wv",
    "wi",
    "wy",
]
title = [
    "Title_Status",
    "clean",
    "rebuilt",
    "lien",
    "salvage",
    "parts only",
    "missing",
]
transmission = [
    "Transmission",
    "automatic",
    "other",
    "manual",
]
car_type = [
    "Type",
    "SUV",
    "mini-van",
    "convertible",
    "coupe",
    "truck",
    "wagon",
    "sedan",
    "pickup",
    "hatchback",
    "van",
    "other",
    "bus",
    "offroad",
]
year = "Year"

# Set up flask
app = Flask(__name__)


def send_machine_learning_data(vehicle):
    if vehicle == None:
        print("No data!", flush=True)
        return

    print(vehicle, flush=True)

    machine_learning_data = {
        # "id",
        # "region",
        # "price",
        "year": int(vehicle["year"]),
        # "manufacturer",
        # "model",
        "condition": int(vehicle_condition_map[vehicle["condition"]]),
        # "cylinders",
        # "fuel",
        "odometer": int(vehicle["odometer"]),
        # "title_status",
        "transmission": vehicle["transmission"],
        "size": int(vehicle_size_map[vehicle["size"]]),
        "type": vehicle["car_type"],
        # "paint_color",
        "state": vehicle["state"].lower(),
        # "lat",
        # "long",
        # "posting_date",
        "fwd": 1 * (cyl.index(vehicle["cyl"]) == 1 or cyl.index(vehicle["cyl"]) == 3),
        "rwd": 1 * (cyl.index(vehicle["cyl"]) == 2 or cyl.index(vehicle["cyl"]) == 3),
    }

    print(machine_learning_data, flush=True)
    print(machine_learning_data, flush=True)
    print(machine_learning_data, flush=True)
    print(machine_learning_data, flush=True)

    result = submit_model(
        machine_learning_data,
        [
            "year",
            "condition",
            "odometer",
            "transmission",
            "size",
            "type",
            "state",
            "fwd",
            "rwd",
        ],
        "Used_Car_Price_Pipeline_SVR.pkl",
    )

    return redirect("/" + str(result), code=302)


def convertFormToVehicle(formData):
    formData = formData.replace("%20", " ")
    rawDataFields = formData.split("&")
    vehicle = {}
    if "year=" + year in rawDataFields:
        return None
    if "odometer=" + odometer in rawDataFields:
        return None
    for rawData in rawDataFields:
        var_name, var_value = rawData.split("=")
        if globals()[var_name][0] == var_value:
            print(f"Missing value for {var_name}: got {var_value}", flush=True)
            return None
        vehicle[var_name] = var_value
    return vehicle


@app.route("/postmethod", methods=["POST"])
def post_javascript_data():
    return {
        "color": color,
        "condition": condition,
        "cyl": cyl,
        "fuel_type": fuel_type,
        "manufacturer": manufacturer,
        "odometer": odometer,
        "size": size,
        "state": state,
        "title": title,
        "transmission": transmission,
        "car_type": car_type,
        "year": year,
    }


@app.route("/")
@app.route("/<money>")
def index(money=None):
    try:
        cash = float(money)
        money = f"${cash}"
    except:
        money = ""
    return render_template("index.html", money=money)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/submit/<formData>")
def submit(formData):
    print(formData, flush=True)
    vehicle = convertFormToVehicle(formData)
    return send_machine_learning_data(vehicle)


if __name__ == "__main__":
    app.run(debug=True)
