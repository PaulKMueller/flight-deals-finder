import datetime as dt
import requests
from requests.auth import HTTPBasicAuth
import json
import yaml

with open("config.yml") as file:
    config = yaml.safe_load(file)
    SHEETY_USER =  config["SHEETY_USER"]
    SHEETY_PASSWORD = config["SHEETY_PASSWORD"]
    AUTH_SHEETY = config["AUTH_SHEETY"]
    SHEETY_ENDPOINT = config["SHEETY_ENDPOINT"]
    KIWI_API_KEY = config["KIWI_API_KEY"]
    KIWI_ENDPOINT = config["KIWI_ENDPOINT"]
    HOMETOWN_IATA = config["HOMETOWN_IATA"]


#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

basic_auth = HTTPBasicAuth(SHEETY_USER, SHEETY_PASSWORD)

headers = {
    "Authorization": AUTH_SHEETY
}

# sheet_data = requests.get(SHEETY_ENDPOINT, headers=headers, auth=basic_auth).json()["prices"]

# def getIataCodeForCity(city: str) -> str:
#     with open("parsed.json", encoding="utf-8") as file:
#         iata_dict = json.load(file)
#         iata_dict = dict((y, x) for x, y in iata_dict.items())
#     return iata_dict[city]

# for entry in sheet_data:
#     body = {
#         "price":{
#             "iataCode": getIataCodeForCity(entry['city'])
#             }
#         }
#     response = requests.put(SHEETY_ENDPOINT + f"/{entry['id']}", json=body, headers=headers, auth=basic_auth)
#     print(response)
# print(sheet_data)

sheet_data = requests.get(SHEETY_ENDPOINT, headers=headers, auth=basic_auth).json()["prices"]
print(sheet_data)

for entry in sheet_data:
    today = dt.datetime.today()
    today_string = today.strftime("%d/%m/%Y")
    till_day = today + dt.timedelta(weeks=26)
    till_day_string = till_day.strftime("%d/%m/%Y")


    headers = {
        "apikey": KIWI_API_KEY
    }

    body = {
        "fly_from": HOMETOWN_IATA,
        "fly_to": entry["iataCode"],
        "date_from": today_string,
        "date_to": till_day_string
    }

    kiwi_response = requests.get(KIWI_ENDPOINT, params=body, headers=headers)
    for flight in kiwi_response.json()["data"]:
        if float(flight["price"]) < float(entry["lowestPrice"]):
            print(f"Flight {flight['id']} to {flight['cityTo']}")
        else:
            print("Too expensive")
