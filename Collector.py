"""
Collector functionality.
Collecting data from Current Weather and loads it into CityWeather list
"""
import requests
from datetime import datetime

"""
RESP API function
Takes city ID.
Returns a dictionary with the weather data.
"""


def get_current_city_weather(city_id):
    weather_data = {"time": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "threshold_met": False}

    resp = requests.get(
        'https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_key}&units=metric'.format(city_id=city_id, API_key="e735b6b632e6c008be941b8dbdb346d4"))

    if resp.status_code == 429:
        print("OpenWeather database is experiencing too many requests from this machine, please try running "
              "Weather Tracker at another time")
        exit()
    if resp.status_code != 200:
        print("Cannot fetch this city's weather, received status code {}".format(resp.status_code))
        return {}

    response = resp.json()
    weather_data["city_name"] = response["name"]
    weather_data["temperature"] = response["main"]["temp"]
    weather_data["wind_speed"] = response["wind"]["speed"]

    return weather_data


"""
Gets the needed data from RESP API function and loads it into CityWeather map.
Takes CityWeather and REST API data.
Returns True.
"""


def load_city_weather(city_weather, city_id):
    new_weather = get_current_city_weather(city_id)

    if new_weather:
        city_weather.put_data(new_weather)
        return True
    else:
        print("Error fetching city weather")
        return False
