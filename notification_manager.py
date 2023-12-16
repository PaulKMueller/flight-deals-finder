import smtplib
import yaml
from data_manager import DataManager

with open("config.yml") as file:
    config = yaml.safe_load(file)
    MY_EMAIL = config["MY_EMAIL"]
    MY_EMAIL_PASSWORD = config["MY_EMAIL_PASSWORD"]
    SHEETY_ENDPOINT_USERS = config["SHEETY_ENDPOINT_USERS"]
    

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def notify_about_flights(self, flights: list, data_manager: DataManager):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_EMAIL_PASSWORD)
            for address in data_manager.get_user_emails():
                connection.sendmail(from_addr=MY_EMAIL, to_addrs=address, msg=str(flights))
