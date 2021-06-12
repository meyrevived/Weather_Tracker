"""
Collector functionality.
Collecting data from Current Weather and loads it into CityWeather list
"""
import requests
from datetime import datetime
from multiprocessing import Process

weather_data = {}
network_error = False


def get_current_city_weather(city_id, stop, run_api_key):
    """
    RESP API function with ability to stop Weather Tracker is connection issues are experienced.
    Takes city ID, Stop and ApiKey.
    Appends weather data to weather_data.
    """

    try:
        weather_data["time"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        weather_data["threshold_met"] = False

        resp = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_key}&units=metric'
            ''.format(city_id=city_id, API_key=run_api_key))

        if resp.status_code == 429:
            print("OpenWeather database is experiencing too many requests from this machine, please try running "
                  "Weather Tracker at another time")
            stop.stop_all = True
        if resp.status_code != 200:
            print("Cannot fetch this city's weather, received status code {}".format(resp.status_code))
            return

        response = resp.json()
        weather_data["city_name"] = response["name"]
        weather_data["temperature"] = response["main"]["temp"]
        weather_data["wind_speed"] = response["wind"]["speed"]

    except Exception as e:
        print("Weather Tracker is experiencing {err}".format(err=e.__class__.__name__))
        print("Please fix connection issues in your machine and try Weather Tracker again")
        stop.say_goodbye()
        exit()


def load_city_weather(city_weather, city_id, stop, run_api_key):
    """
    Gets the needed data from RESP API function and loads it into CityWeather map.
    Takes CityWeather, city_id, Stop and ApiKey.
    Runs get_current_city_weather with a timeout to escape connection issues.
    Attempts collecting weather data five times before declaring that collection is importable.
    Returns True or False depending on its successful status.
    """
    failed_runs = 0

    collection_process = Process(get_current_city_weather(city_id, stop, run_api_key))
    collection_process.start()
    collection_process.join(120)
    if collection_process.is_alive():
        print("Connection to OpenWeather database is taking too long, terminating collection processes")
        collection_process.terminate()
        stop.stop_all = True
        collection_process.join()

    while failed_runs < 5 or not stop.stop_all:
        if weather_data:
            city_weather.put_data(weather_data)
            return True
        else:
            print("Error fetching city weather for {city}".format(city=city_id))
            failed_runs += 1

    return False
