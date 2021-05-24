"""
Manager script.
Parses configuration JSON into internal variables.
Creates CityWeather objects according to configurations in configuration JSON.
Creates Monitors per CityWeather and sets them running.
"""
import json
import time

from CityWeather import CityWeather
from Monitor import Monitor

"""
Creates a Monitor with a CityWeather to handle.
Takes the city_id, frequency, city_weather and threshold from a dictionary from configuration_json.
Returns True.
"""


def create_monitor(city_weather, city_weather_dict):
    return Monitor(city_weather_dict["frequency"], city_weather_dict["threshold"], city_weather)


"""
Creates a CityWeather object with a city_id.
Takes city_id from a dictionary from configuration_json.
Returns True.
"""


def create_city_weather(city_weather_dict):
    return CityWeather(city_weather_dict["city_id"])


"""
Parses each dictionary in the configuration JSON and loads its values to city_id, city_name, frequency and threshold.
Fetches the configuration JSON from the file system. 
Takes each configuration section in the JSON file and turns it into a dictionary with the same data in the list 
configuration_json.
Returns configuration_json.
"""


def configuration_parser(configuration_file):
    configuration_json = []

    try:
        with open(configuration_file, 'r') as config_json:
            config_data = json.load(config_json)
            for item in config_data:
                item = {"city_id": item["city_id"], "city_name": item["city_name"],
                        "frequency": item["frequency"], "threshold": item["threshold"]}
                configuration_json.append(item)

        return configuration_json
    except IOError as e:
        print('{err} occurred when opening {f}'.format(err=repr(e), f=configuration_file))
        return False


"""
Runs the Manager functionality. 
Checks that loading the configuration JSON was successful. 
Creates a Monitor and a CityWeather according the data in each dictionary in configuration_parser's returned 
configuration_json. 
Sets each created Monitor running.
Takes the name of the configuration JSON.
"""


def run_manager(config_file_path):
    config_file = config_file_path
    weather_config_json = configuration_parser(config_file)

    monitor_threads = []

    if weather_config_json:
        for config_dict in weather_config_json:
            city_weather_instance = create_city_weather(config_dict)
            monitor = create_monitor(city_weather_instance, config_dict)
            monitor.daemon = True
            monitor_threads.append(monitor)

    for monitor_thread in monitor_threads:
        time.sleep(20)
        monitor_thread.start()

    try:
        while True:
            time.sleep(.1)
    except (KeyboardInterrupt, SystemExit):
        print()
        print(49 * "X")
        print("XXXXXX Thank you for using Weather Tracker! XXXXXX")
        print(49 * "X")
