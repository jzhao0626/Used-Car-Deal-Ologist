import os
import traceback
import sqlite3
from flask import Flask, render_template, redirect, current_app as app
import json

# Set up flask
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
