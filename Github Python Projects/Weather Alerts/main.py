import requests

from twilio.rest import Client

account_sid = '*****'
auth_token = '****'
APIkey = "******"



params = {
            "lat": 51,
            "lon": -114,
            "appid": APIkey,
            "exclude": "current,minutely,daily"}


def send_rain_sms():
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body='Today there is chance of rain, bring an umbrella!',
        from_='****',
        to='*****'
        )
    print(message.status)


resp = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=params)
resp.raise_for_status()
weather_data = resp.json()

for hour in range(0, 11) :
    if weather_data["hourly"][hour]["weather"][0]["id"] < 900:
        send_rain_sms()
        break


