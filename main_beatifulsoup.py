# use selenium and start web browser firefox
import requests
from bs4 import BeautifulSoup
import db_handler

items_info = []

mongo = db_handler.Main()
mongo.select_database("allegro")

# def clear_json():
#     with open("items.json", "w") as json_file:
#         json_file.write("")

# def repair_json():
#     with open("items.json", "r") as json_file:
#         json_string = json_file.read()

#     without_brackets = json_string.replace("[", "").replace("]", "")
#     final_json_string = "[\n" + without_brackets + "\n]"

#     with open("items.json", "w") as json_file:
#         json_file.write(final_json_string)


def item_info(url, total=False, current=True):
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    if total:
        items_number = soup.find("span", class_="mlc-listing__offer-count__number").text
        print(items_number)
        number_of_pages = round(int(items_number) / 60 + 2, 0)
        return number_of_pages

    items = soup.find_all("article")
    for item in items:
        item_link = item.find("a", class_="mlc-itembox")["href"]
        item_name = item.find("h3").text.replace("\"", "")
        item_price = item.find("span", class_="ml-offer-price__dollars").text
        end_time_element = item.find(
            "span", {"data-mlc-itembox-bidding-remaining-time": True}
        )
        item_timeleft = end_time_element["data-mlc-itembox-bidding-remaining-time"]

        mongo.insert_one(item_name, item_link, item_price, item_timeleft)


def main(category, site):
    print(site)
    if "https://allegrolokalnie.pl/" not in site:
        return "Doesn't look like a valid allegrolokalnie link."
    elif "?typ=licytacja" not in site:
        return "Doesn't have \"?typ=licytacja\" parameter."
    else:
        mongo.select_collection(category)
        site_number = 1
        total = item_info(site, total=True)

        while total > site_number:
            final_link = site + "&page=" + str(site_number)
            item_info(final_link)
            print(f"{site_number}. ", end="", flush=True)
            site_number += 1

        return "Done"


# test = main("allegro_test", "https://allegrolokalnie.pl/oferty/elektronika?typ=licytacja&price_to=10")
# print(test)