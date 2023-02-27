import requests
import os
import datetime as dt

today = dt.datetime.today()
from twilio.rest import Client

account_sid = 'ACf5f818f4ec14e8b34ebc7e9a48557f43'
auth_token = '79e3691e6b388cc6a5c2e887ade4ddd0'

STOCK = "INTC"
COMPANY_NAME = "Intel Corporation"

stock_price_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={STOCK}&apikey=6ZTDUH6PIDA75J1V'
stock_resp = requests.get(stock_price_url)
stock_data = stock_resp.json()["Time Series (Daily)"]
last_day_data = next(iter(stock_data.items()))
# last_day_data = list(stock_data.items())[0]

last_open = last_day_data[1]["1. open"]
last_close = last_day_data[1]["4. close"]
last_day_diff = round((float(last_close) - float(last_open)) / float(last_open) * 100, 2)

news_url = ('https://newsapi.org/v2/everything?'
            'q=INTC stock&'
            #'searchIn=title&'
            f'from={today.date()}&'
            'sortBy=popularity&'
            'language=en&'
            'apiKey=8b522553c7e64ec0ad74b65b24cdda90')

news_resp = requests.get(news_url)
news_resp.raise_for_status()
news_data = news_resp.json()
top_news_article = news_data["articles"][0]
headline = f"Headline: {news_data['articles'][0]['title']}\n"
brief = f"Brief: {news_data['articles'][0]['description']}\n"
link = f"Link: {news_data['articles'][0]['url']}"


if last_day_diff > 0:
    emoj = "🟢"
else:
    emoj = "🟥"

alert = f"{STOCK}: {emoj} {last_day_diff:+g}%\n"

message = str(alert + headline + brief + link)


def send_sms():
    global message
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_='+14793411959',
        to='+15875774686'
    )
    print(message.status)

print(message)