from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w', format='%(asctime)s %(levelname)s - %(message)s', datefmt='[%H:%M:%S]', encoding='utf-8')

def get_database(client, database_name):
    # Access the database
    db = client[database_name]
    return db

class Main:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')

    def select_database(self, database_name):
        self.db = self.client[database_name]

    def select_collection(self, collection_name):
        self.collection = self.db[collection_name]

    def insert_one(self, name, href, price, endTime):
        #correct args
        endTime = Utils.convert_end_time(endTime)
        print("Price:" + price)
        price = int(price.replace(" ", "").replace(",", ""))

        name_dup = self.collection.find_one({"name": name})

        if name_dup == None or name_dup['status'] != "bad_item":
            href_dup = self.collection.find_one({"href": href})
            print(href_dup)
            if href_dup == None:
                self.collection.insert_one({
                    "name": name,
                    "href": href,
                    "price": price,
                    "endTime": endTime,
                    "status": "None"
                })
                logging.info(f"[Success] Insert to database: \"{name}\", \"{href}\", \"{price}\", \"{endTime}\"")
            else:
                duplicate = self.collection.find_one({"href": href, 'status': "bad_price"})
                if duplicate != None:
                    if price < duplicate["price"]:
                        # Update price, status = none, update endTime
                        self.collection.update_one(
                            {"href": href},
                            {"$set": {
                                "price": price,
                                "status": "None",
                                "endTime": endTime,
                            }}
                        )
                        logging.info("[Duplicate found] href - bad_price - price lower, updating price")
                    else:
                        logging.info("[Duplicate found] href - bad_price - no price change, skipping")
                else:
                    logging.info("[Duplicate found] href - skipping")
        else:
            logging.info("[Duplicate found] name - bad item tag, skipping")

class Utils:
    @staticmethod
    def convert_end_time(end_time_str):
        json_obj = json.loads(end_time_str)
        ending_at_str = json_obj["endingAt"]
        ending_at_date = datetime.fromisoformat(ending_at_str.replace("Z", "+00:00"))
        return ending_at_date




#
#       name: Name of item
#       href: Link to item
#       price: Price of item
#       endTime: Time left to end of auction
#       status: Status of item (None, bad_price, bad_item, okay)