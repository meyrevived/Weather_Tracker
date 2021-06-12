"""
Monitor object. exists per CityWeather.
Handles the data in CityWeather.
Notes if there is a delta of Y threshold between temps in CityWeather.
Prints the latest reading in specific format with or without threshold delta alarm.
Clears CityWeather from too much data.
"""
import time
from datetime import datetime, timezone, timedelta

from Collector import load_city_weather
from Utilities import set_task_state_with_lock


class Monitor:

    def __init__(self, frequency, threshold, city_weather, api_key):
        super().__init__()
        self.frequency = frequency
        self.city_weather = city_weather
        self.threshold = threshold
        self.api_key = api_key.get_api_key()

        self.latest_reading = {}
        self.previous_reading = {}

        self.last_run_at = datetime.now(timezone.utc) - timedelta(hours=24, minutes=0)
        self.at_work = False

    def run_collector(self, stop):
        """
        Runs a Collector on the city_id the Monitor is set to.
        Takes a Stop.
        """
        load_city_weather(self.city_weather, self.city_weather.get_city_id(), stop, self.api_key)

    def get_weather_reading(self):
        """
        Loads self.latest_reading with the last thing the Collector put in self.city_weather.
        Loads self.previous_reading with the n-1 dictionary from self.city_weather.
        """
        self.latest_reading = self.city_weather.get_latest()

        if self.city_weather.weather_deque_size() >= 2:
            self.previous_reading = self.city_weather.get_previous()

    def check_for_threshold_delta(self):
        """
        Checks for desired threshold delta between the temperature fields in self.previous_reading and self.latest_reading.
        If such a delta is found, updates self.latest_reading's threshold_met key to True
        """
        if self.city_weather.weather_deque_size() >= 2:
            if abs(self.previous_reading["temperature"] - self.latest_reading["temperature"]) >= self.threshold:
                self.latest_reading["threshold_met"] = True

    def print_latest_reading(self):
        """
        Prints self.latest_reading to screen.
        If threshold_met key has value of True adds an additional warning line to printed data
        """
        if self.city_weather.get_deque_len() > 2:
            print(50 * "*")
            for key, value in self.latest_reading.items():

                if key != "threshold_met":
                    print('{k}: {v}'.format(k=key, v=value))
                else:
                    if value:
                        print('ATTENTION: temperature change of {} degrees!'.format(self.threshold))
            print(50 * "*")

    def city_weather_size_monitor(self):
        """
        Checks if self.city_weather has reached over 50 weather reading dictionaries and deletes whatever has accumulated
        beyond 50.
        """
        city_weather_length = self.city_weather.weather_deque_size() - 50

        if city_weather_length > 50:
            self.city_weather.delete_data(city_weather_length)

    def run_monitor(self, stop, manager):
        """
        Makes the created Monitor run. Handles the lock from utility to allow smooth running.
        Takes a Stop and a Manager
        """
        error_counter = 0

        self.run_collector(stop)
        try:
            if error_counter < 5:
                self.get_weather_reading()
                self.check_for_threshold_delta()
                self.print_latest_reading()
                self.city_weather_size_monitor()
            else:
                print('Experiencing too many errors fetching weather data for '
                      '{city}'.format(city=self.city_weather.get_city_id()))
                print('Please check configuration and try running Weather Tracker again')
                stop.stop_all = True
        except Exception as e:
            print('{err} occurred while getting weather data for {city_weather}'
                  ''.format(err=repr(e), city_weather=self.city_weather.get_city_id()))
            error_counter += 1
        finally:
            self.last_run_at = datetime.now(timezone.utc)
            set_task_state_with_lock(manager, self, False)
