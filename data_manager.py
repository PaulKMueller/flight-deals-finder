import yaml
import requests
from requests.auth import HTTPBasicAuth
import json

with open("config.yml") as file:
    config = yaml.safe_load(file)
    SHEETY_USER =  config["SHEETY_USER"]
    SHEETY_PASSWORD = config["SHEETY_PASSWORD"]
    AUTH_SHEETY = config["AUTH_SHEETY"]
    SHEETY_ENDPOINT_PRICES = config["SHEETY_ENDPOINT_PRICES"]
    SHEETY_ENDPOINT_USERS = config["SHEETY_ENDPOINT_USERS"]
    KIWI_API_KEY = config["KIWI_API_KEY"]
    KIWI_ENDPOINT = config["KIWI_ENDPOINT"]
    HOMETOWN_IATA = config["HOMETOWN_IATA"]

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.basic_auth = HTTPBasicAuth(SHEETY_USER, SHEETY_PASSWORD)
        self.headers = {
            "Authorization": AUTH_SHEETY
        }
        self.sheet_data = self.get_sheet_data()

    def get_sheet_data(self):
        return requests.get(SHEETY_ENDPOINT_PRICES, headers=self.headers, auth=self.basic_auth).json()["prices"]
    

    def upload_user(self, first_name, last_name, email):
        user = {
            "user": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email
            }
        }

        response = requests.post(SHEETY_ENDPOINT_USERS, json=user, headers=self.headers, auth=self.basic_auth)
    
    def fill_in_iata(self):
        for entry in self.sheet_data:
            body = {
                "price":{
                    "iataCode": self.getIataCodeForCity(entry['city'])
                    }
                }
            response = requests.put(SHEETY_ENDPOINT_PRICES + f"/{entry['id']}", json=body, headers=self.headers, auth=self.basic_auth)

    @staticmethod
    def getIataCodeForCity(city: str) -> str:
        with open("parsed.json", encoding="utf-8") as file:
            iata_dict = json.load(file)
            iata_dict = dict((y, x) for x, y in iata_dict.items())
        return iata_dict[city]