import requests
import datetime as dt
import os



APP_ID = os.environ.get("NUTRITIONIX_APP_ID")
API_KEY = os.environ.get("NUTRITIONIX_API_KEY")
SHEETY_TOKEN = os.environ.get("SHEETY_TOKEN")
SHEETY_ID = os.environ.get("SHEETY_ID")

endpoint_url = "https://trackapi.nutritionix.com/v2/natural/exercise"
QUERY = "ran 10 miles and cycled 20 minutes"#input("What activity(ies) did you complete")

nutri_headers = {"x-app-id": APP_ID,
           "x-app-key": API_KEY,
           }

nutri_params = {
 "query": QUERY,
 "gender":"male",
 "weight_kg":72,
 "height_cm":172,
 "age":29
}

sheety_api = f"https://api.sheety.co/{SHEETY_ID}/workoutsTracker/workouts"



nutri_resp = requests.post(url=endpoint_url, headers=nutri_headers, json=nutri_params)

list = nutri_resp.json()
sheety_headers = {
    "Authorization": f"Bearer {SHEETY_TOKEN}"
}

for exercise in range(0,len(list["exercises"])):
    ex_type = str(list["exercises"][exercise]['name']).title()
    duration = str(list["exercises"][exercise]['duration_min'])
    calories = str(list["exercises"][exercise]['nf_calories'])

    workout_params = {
      "workout": {
        "date": dt.datetime.today().date().strftime('%d/%m/%Y'),
        "time": dt.datetime.now().strftime('%H:%M'),
        "exercise": ex_type,
        "duration": duration,
        "calories": calories

      }
    }

    sheety_resp = requests.post(url=sheety_api, json=workout_params, headers=sheety_headers)

    print(sheety_resp.text)