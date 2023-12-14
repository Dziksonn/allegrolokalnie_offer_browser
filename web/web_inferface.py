from flask import Flask, render_template
import os, sys, inspect
from bson import json_util
import json

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import db_handler

mongo = db_handler.Main()
mongo.select_database("allegro")

app = Flask(__name__)


def parse_json(data):
    return json.loads(json_util.dumps(data))


class DataStore:
    sorted_list = []
    sorted_good_list = []


data = DataStore()


# web section
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/offer_browser")
def offer_browser():
    return render_template("offer_browser.html")


@app.route("/good_items")
def good_items():
    return render_template("good_items.html")


# api section
@app.route("/api/get_good_items")
def get_good_items():
    return_data = []
    for x in data.sorted_good_list:
        return_data.append(
            {
                "name": x["name"],
                "href": x["href"],
                "price": x["price"],
                "endTime": x["endTime"],
            }
        )
    return json.dumps(return_data)


@app.route("/api/get_item")
def get_item():
    if len(data.sorted_list) == 0:
        return "No more items", 400
    else:
        return data.sorted_list[0]["href"], 200


@app.route("/api/get_collections")
def get_collections():
    return mongo.db.list_collection_names()


@app.route("/api/select_collection/<collection>")
def select_collection(collection):
    mongo.select_collection(collection)
    data.sorted_list = parse_json(mongo.get_sorted_list())
    data.sorted_good_list = parse_json(mongo.get_sorted_list("good"))
    print(data.sorted_good_list)
    return "Success", 200


@app.route("/api/set_status/<status>")
def set_status(status):
    if status == "bad_item":
        mongo.set_status(data.sorted_list[0]["href"], "bad_item")
        pass
    elif status == "bad_price":
        mongo.set_status(data.sorted_list[0]["href"], "bad_price")
        pass
    elif status == "good":
        mongo.set_status(data.sorted_list[0]["href"], "good")
        pass
    elif status == "skip":
        pass
    else:
        return "Invalid status", 400
    data.sorted_list.pop(0)
    return "Success", 200


if __name__ == "__main__":
    app.run(debug=True)
