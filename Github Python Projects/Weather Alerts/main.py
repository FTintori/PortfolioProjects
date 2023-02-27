import requests

from twilio.rest import Client

account_sid = 'ACf5f818f4ec14e8b34ebc7e9a48557f43'
auth_token = '79e3691e6b388cc6a5c2e887ade4ddd0'
APIkey = "69f04e4613056b159c2761a9d9e664d2"
#"36d615cbd7cbda21fd3b478d2bab9f77"
# "69f04e4613056b159c2761a9d9e664d2"


params = {
            "lat": 51.080244,
            "lon": -114.146742,
            "appid": APIkey,
            "exclude": "current,minutely,daily"}


def send_rain_sms():
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body='Today there is chance of rain, bring an umbrella!',
        from_='+14793411959',
        to='+15875774686'
        )
    print(message.status)


resp = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=params)
resp.raise_for_status()
weather_data = resp.json()

for hour in range(0, 11) :
    if weather_data["hourly"][hour]["weather"][0]["id"] < 900:
        send_rain_sms()
        break


