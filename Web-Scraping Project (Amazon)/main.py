import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import datetime
import csv
import smtplib
import os

# CREATE FILE FOR PRICE LOG

# header = ['Item_Name', 'Price', 'Date_added']
# with open('Amazon_webscrape.csv', 'w', newline='', encoding='UTF8') as f:
#     writer = csv.writer(f)
#     writer.writerow(header)

URL = 'https://www.amazon.com/WDIRARA-Womens-Cartoon-Sleeve-Multicolored/dp/B08SQ5D232/ref=sr_1_19_sspa?crid=JUGEMB8LZ6U&keywords=cow%2Bshirt&qid=1663717496&sprefix=cow%2Bshir%2Caps%2C197&sr=8-19-spons&smid=A34CQ7S73A4TP4&th=1&psc=1'

def record_price():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"
    }

    page = requests.get(URL, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    title = soup2.find(id = 'productTitle').get_text().strip()
    price = float(soup2.find(class_ = 'a-offscreen').get_text().strip()[1:])
    date = datetime.date.today()
    data = [title, price, date]

    with open('Amazon_webscrape.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

        df = pd.read_csv(r'C:\Users\zio_p\PycharmProjects\pythonProject\AtA Web Scraping (Amazon)\Amazon_webscrape.csv')
        print(df)
        return price

def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    # server.starttls()
    server.ehlo()
    server.login('francesco.tintori93@gmail.com', os.environ("PASSCODE"))

    subject = "Price Drop!"
    body = f"The item you have been tracking at {URL} has dropped in price!"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'francesco.tintori93@gmail.com',
        'francesco.tintori93@gmail.com',
        msg
    )

while (True):
    if record_price() < 20:
        send_mail()
    time.sleep(3600)
