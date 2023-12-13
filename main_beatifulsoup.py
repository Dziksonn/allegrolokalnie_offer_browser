#use selenium and start web browser firefox
import requests
from bs4 import BeautifulSoup
import time
import json

items_info = []

def clear_json():
    with open("items.json", "w") as json_file:
        json_file.write("")

def repair_json():
    with open("items.json", "r") as json_file:
        json_string = json_file.read()

    without_brackets = json_string.replace("[", "").replace("]", "")
    final_json_string = "[\n" + without_brackets + "\n]"

    with open("items.json", "w") as json_file:
        json_file.write(final_json_string)

def item_info(url):
    response = requests.get(url)
    response.encoding = 'utf-8'  # Manually set the encoding to UTF-8
    soup = BeautifulSoup(response.text, 'html.parser')

    # Rest of your code...

    items = soup.find_all('article')
    for item in items:
        item_link = item.find('a', class_='mlc-itembox')['href']
        item_name = item.find('h3').text
        item_price = item.find('span', class_='ml-offer-price__dollars').text
        end_time_element = item.find('span', {'data-mlc-itembox-bidding-remaining-time': True})
        item_timeleft = end_time_element['data-mlc-itembox-bidding-remaining-time']

        items_info.append({
            "name": item_name,
            "href": item_link,
            "price": item_price,
            "endTime": item_timeleft
        })

def main():
    site = input("Wklej link: ")
    clear_json()
    # site = "https://allegrolokalnie.pl/oferty/moda/uzywane?typ=licytacja"
    if 'https://allegrolokalnie.pl/' not in site:
        print("Nieprawidłowy link, to nie allegro lokalnie")
        main()
    elif '?typ=licytacja' not in site:
        print("Nieprawidłowy link, to nie licytacja")
        main()
    else:
        site_number = 1
        while True:
            try:
                final_link = site + "&page=" + str(site_number)
                item_info(final_link)
                print(f"{site_number}. ", end='', flush=True)
                site_number += 1
            except:
                print("Koniec")
                with open("items.json", "a") as json_file:
                    json.dump(items_info, json_file, indent=2)
                # repair_json()
                break

main()
