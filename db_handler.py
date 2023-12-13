from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import logging

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w', format='%(asctime)s %(levelname)s - %(message)s', datefmt='[%H:%M:%S]')

def connect_to_database():
    # Connect to the MongoDB server
    client = MongoClient('mongodb://localhost:27017/')
    return client

def get_database(client, database_name):
    # Access the database
    db = client[database_name]
    return db

class DBHandler:
    def __init__(self):
        self.client = connect_to_database()

    def select_database(self, database_name):
        self.db = get_database(self.client, database_name)

    def select_collection(self, collection_name):
        self.collection = self.db[collection_name]

    def insert_one(self, name, href, price, endTime):
        price = int(price)
        try:
            self.collection.insert_one({
                "name": name,
                "href": href,
                "price": price,
                "endTime": endTime,
                "status": "None"
            })
            logging.info("Inserted to database")
        except DuplicateKeyError:
            duplicate = self.collection.find_one({"href": href})
            if duplicate["status"] == "bad_price":
                if price < duplicate["price"]:
                    # Update price, status = none, update endTime
                    self.collection.update_one(
                        {"href": href},
                        {"$set": {
                            "price": price,
                            "status": "None",
                            "endTime": endTime
                        }}
                    )
                    logging.info("Duplicate found, updating price")
                else:
                    logging.info("Duplicate found, no price change, skipping")
            else:
                logging.info("Duplicate found, no bad price tag, skipping")
        except Exception as e:
            logging.error("Error while inserting to database: " + str(e))


    def __del__(self):
        self.client.close()


mongo = DBHandler()
mongo.select_database('allegro')
mongo.select_collection('allegro_test')

print(mongo.insert_one("test", "test", "123", "test"))




#
#       name: Name of item
#       href: Link to item
#       price: Price of item
#       endTime: Time left to end of auction
#       status: Status of item (None, bad_price, bad_item, okay)