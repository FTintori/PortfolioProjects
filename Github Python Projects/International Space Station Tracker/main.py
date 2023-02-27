import requests
from datetime import datetime
import smtplib
from time import sleep
my_email = "****@gmail.com"
MY_LAT = 51
MY_LNG = -114
resp = requests.get("http://api.open-notify.org/iss-now.json")
resp.raise_for_status()

data = resp.json()
iss_longitude = float(data["iss_position"]["longitude"])
iss_latitude = float(data["iss_position"]["latitude"])

iss_position = (iss_latitude, iss_longitude,)


params = {
            "lat": MY_LAT,
            "lng": MY_LNG,
            "formatted": 0
}
resp_sun = requests.get("https://api.sunrise-sunset.org/json", params=params)
resp_sun.raise_for_status()
sunrise = resp_sun.json()["results"]["sunrise"]
sunrise_hour = int((sunrise.split("T")[1]).split(":")[0])-7
sunset = resp_sun.json()["results"]["sunset"]
sunset_hour = int((sunset.split("T")[1]).split(":")[0])-7


time_now = datetime.now()

is_night_time = time_now.hour > sunset_hour or time_now.hour < sunrise_hour
def iss_close():
    iss_close = abs(MY_LAT - iss_latitude) < 5 and abs(MY_LNG - iss_longitude) < 5
    return iss_close

def send_email():
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
        server.ehlo()
        # server.starttls()
        server.ehlo()
        server.login(my_email, "hfvmawpgrjmgcvtv")
        subject = f"Look UP! ISS is in the sky!"
        body = "The ISS should be visible in the sky right now. You should look!"
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail(
            '****@gmail.com',
            '****@gmail.com',
            msg
        )


while True:
    if iss_close() and is_night_time:
        send_email()
        sleep(5)
    elif not is_night_time:
        sleep(3600)
    elif is_night_time and not iss_close():
        sleep(300)

print(iss_position)
