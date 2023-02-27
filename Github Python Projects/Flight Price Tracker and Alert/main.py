# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import requests
import datetime as dt
from pprint import pprint
import os
from twilio.rest import Client

account_sid = 'ACf5f818f4ec14e8b34ebc7e9a48557f43'
auth_token = '79e3691e6b388cc6a5c2e887ade4ddd0'
# api.tequila.kiwi.com/v2/search
TEQUILA_KEY = "WzD0MweacybzENjQB4RpDwSE74GqLtfa"

SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
SHEETY_ID = os.environ.get("SHEETY_ID")

sheety_headers = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"}

tequila_headers = {
    "apikey": TEQUILA_KEY,
}

sheety_api = f"https://api.sheety.co/{SHEETY_ID}/flightSearch/prices"

trip_params = {
    "price": {
        "city": "",
        "iataCode": "",
        "lowestPrice": ""
    }
}

sheety_resp = requests.get(url=sheety_api, json=trip_params, headers=sheety_headers)

sheet_data = sheety_resp.json()

def send_sms():
    global message
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_='+14793411959',
        to='+15875774686'
    )
    print(message.status)

for _ in range(0, len(sheet_data["prices"])):
    if sheet_data["prices"][_]["iataCode"] == "":
        sheety_apii = f"https://api.sheety.co/{SHEETY_ID}/flightSearch/prices/{_ + 2}"
        current_city = sheet_data["prices"][_]["city"]
        tequila_param = {
            "term": f"{current_city}",
            "location_types": "city"
        }

        tequila_api_code_search = "https://api.tequila.kiwi.com/locations/query"
        tequila_resp = requests.get(url=tequila_api_code_search, params=tequila_param, headers=tequila_headers)

        current_code = tequila_resp.json()['locations'][0]['code']

        p_params = {
            "price": {
                "iataCode": f"{current_code}"
            }
        }
        sheety_resp_pyt = requests.put(url=sheety_apii, json=p_params, headers=sheety_headers)

today_prices = {}
for _ in range(0, len(sheet_data["prices"])):
    try:
        sheety_apii = f"https://api.sheety.co/{SHEETY_ID}/flightSearch/prices/{_ + 2}"
        current_city = sheet_data["prices"][_]["iataCode"]
        tequila_api_search = "https://api.tequila.kiwi.com/v2/search"
        flight_param = {
            "fly_from": "YYC",
            "fly_to": f"{current_city}",
            "date_from": (dt.datetime.now()+ dt.timedelta(days = 1)).strftime('%d/%m/%Y'),
            "date_to": (dt.datetime.now()+ dt.timedelta(days = 180)).strftime("%d/%m/%Y"),
            "return_from": (dt.datetime.now()+ dt.timedelta(days = 8)).strftime("%d/%m/%Y"),
            "return_to": (dt.datetime.now()+ dt.timedelta(days = 208)).strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            # "adults": 1,
            "curr": "CAD",
            # "price_to": 1500,
            "max_stopovers": 2,
        }
        tequila_resp = requests.get(url=tequila_api_search, params=flight_param, headers=tequila_headers)
        today_prices[current_city] = tequila_resp.json()['data'][0]['price']

        if int(tequila_resp.json()['data'][0]['price']) < sheet_data["prices"][_]["lowestPrice"]:
            message = f"A flight to {current_city} is available for the price of {int(tequila_resp.json()['data'][0]['price'])}"
            send_sms()
    except IndexError:
        pass





    # print(sheet_data["prices"][_]["city"] + ": " +str(tequila_resp.json()['data'][0]['price']))



