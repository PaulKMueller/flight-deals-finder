import datetime as dt
import requests
from requests.auth import HTTPBasicAuth
import json
import yaml
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

print("\nWelcome to Paul's Flight Club!")
print("We find the best flight deals to your favorite locations and notify you about them.\n")
first_name = input("What is your first name?\n")
last_name = input("What is you last name?\n")

email = input("What is you email?\n")
confirm_email = input("Please confirm your email by typing it again.\n")

if email == confirm_email:
    data_manager.upload_user(first_name, last_name, email)

cities = data_manager.get_sheet_data()

for city in cities:
    notification_manager.notify_about_flights(flight_search.get_next_six_months_flights_to(city["iataCode"], city["lowestPrice"]), data_manager)
