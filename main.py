import datetime as dt
import requests
from requests.auth import HTTPBasicAuth
import json
import yaml
from data_manager import DataManager

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

data_manager = DataManager()

for entry in data_manager.sheet_data:
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
