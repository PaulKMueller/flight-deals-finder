import requests
import yaml
import datetime as dt

with open("config.yml") as file:
    config = yaml.safe_load(file)
    SHEETY_USER =  config["SHEETY_USER"]
    SHEETY_PASSWORD = config["SHEETY_PASSWORD"]
    AUTH_SHEETY = config["AUTH_SHEETY"]
    SHEETY_ENDPOINT = config["SHEETY_ENDPOINT"]
    KIWI_API_KEY = config["KIWI_API_KEY"]
    KIWI_ENDPOINT = config["KIWI_ENDPOINT"]
    HOMETOWN_IATA = config["HOMETOWN_IATA"]

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.headers = {
            "apikey": KIWI_API_KEY
        }

    def get_next_six_months_flights_to(self, iata_code: str, maximum_price: float) -> list:
        """Returns a list of flights gathered from the KIWI 
        flight search API that are below our maximum price.

        Args:
            iata_code (str): The IATA code of the location we want to fly to.
            maximum_price (float): The maximum price we are willing to pay for our flight.

        Returns:
            list: A list of flights gathered from the KIWI API.
        """        
        today = dt.datetime.today()
        today_string = today.strftime("%d/%m/%Y")
        till_day = today + dt.timedelta(weeks=26)
        till_day_string = till_day.strftime("%d/%m/%Y")
        body = {
            "fly_from": HOMETOWN_IATA,
            "fly_to": iata_code,
            "date_from": today_string,
            "date_to": till_day_string
        }

        kiwi_response = requests.get(KIWI_ENDPOINT, params=body, headers=self.headers)
        cheap_flights = []
        for flight in kiwi_response.json()["data"]:
            if float(flight["price"]) < maximum_price:
                print(f"Flight {flight['id']} to {flight['cityTo']}")
                cheap_flights.append(flight)
            else:
                print("Too expensive")

        return cheap_flights