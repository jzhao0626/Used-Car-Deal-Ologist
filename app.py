import os
import traceback
import sqlite3
from flask import Flask, render_template, redirect, current_app as app
import json

error_text = "PLEASE FILL OUT ALL THE DATA"

color = ["Color", "blue", "white", "grey", "black", "brown", "red",
         "silver", "green", "yellow", "purple", "custom", "orange"]
condition = ["Condition", "New", "Like New",
             "Excellent", "Good", "Fair", "Salvage"]
cyl = ["Cylinder", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
fuel_type = ["Fuel_Type", "Electric", "Gas", "Diesel", "Other"]
manufacturer = ["Make", "bmw", "toyota", "honda", "chevrolet", "mazda", "ford", "volvo", "cadillac", "saturn", "subaru", "dodge", "gmc", "ram", "chrysler", "mercedes-benz", "infiniti", "jeep", "buick", "nissan", "volkswagen",
                "mercury", "hyundai", "lexus", "porsche", "rover", "audi", "fiat", "mini", "mitsubishi", "lincoln", "jaguar", "kia", "pontiac", "acura", "tesla", "alfa-romeo", "datsun", "harley-davidson", "land rover", "aston-martin", "ferrari"]
odometer = "Odometer"
size = ["Vehicle_Size", "Compact", "Sub-Compact", "Mid-Size", "Full-Size"]
state = ["State", "al", "ak", "az", "ar", "ca", "co", "ct", "dc", "de", "fl", "ga", "hi", "id", "il", "in", "ia", "ks", "ky", "la", "me", "md", "ma", "mi", "mn",
         "ms", "mo", "mt", "nc", "ne", "nv", "nj", "nm", "ny", "nh", "nd", "oh", "ok", "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy"]
title = ["Title_Status", "Clean", "Rebuilt",
         "Lien", "Salvage", "Parts Only", "Missing"]
transmission = ["Transmission", "Automatic", "Other", "Manual"]
car_type = ["Type", "SUV", "mini-van", "convertible", "coupe", "truck",
            "wagon", "sedan", "pickup", "hatchback", "van", "other", "bus", "offroad"]
year = "Year"

# Set up flask
app = Flask(__name__)


@app.route('/postmethod', methods=['POST'])
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
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/submit/<formData>")
def submit(formData):
    print(formData)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
