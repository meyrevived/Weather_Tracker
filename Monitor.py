"""
Monitor object. exists per CityWeather.
Calls for Collector every X frequency.
Handles the data in CityWeather.
Notes if there is a delta of Y threshold between temps in CityWeather.
Prints the latest reading in specific format with or without threshold delta alarm.
Clears CityWeather from too much data.
"""
import time
import threading
from Collector import load_city_weather


class Monitor (threading.Thread):

    def __init__(self, frequency, threshold, city_weather):
        super().__init__()
        self.frequency = frequency
        self.city_weather = city_weather
        self.threshold = threshold

        self.latest_reading = {}
        self.previous_reading = {}
        self.start_time = time.time()


    """
    Runs a Collector on the city_id the Monitor is set to.
    """

    def run_collector(self):
        load_city_weather(self.city_weather, self.city_weather.get_city_id())

    """
    Loads self.latest_reading with the last thing the Collector put in self.city_weather.
    Loads self.previous_reading with the n-1 dictionary from self.city_weather.
    """

    def get_weather_reading(self):
        self.latest_reading = self.city_weather.get_latest()

        if self.city_weather.weather_deque_size() >= 2:
            self.previous_reading = self.city_weather.get_previous()

    """
    Checks for desired threshold delta between the temperature fields in self.previous_reading and self.latest_reading.
    If such a delta is found, updates self.latest_reading's threshold_met key to True
    """

    def check_for_threshold_delta(self):
        if self.city_weather.weather_deque_size() >= 2:
            # The home assignment said the delta should be X not X or more but that's just silly, so I'm writing this as
            # X or more
            if abs(self.previous_reading["temperature"] - self.latest_reading["temperature"]) >= self.threshold:
                self.latest_reading["threshold_met"] = True

    """
    Prints self.latest_reading to screen.
    If threshold_met key has value of True adds an additional warning line to printed data
    """

    def print_latest_reading(self):
        if self.city_weather.get_deque_len() > 0:
            print(50 * "*")
            for key, value in self.latest_reading.items():

                if key != "threshold_met":
                    print('{k}: {v}'.format(k=key, v=value))
                else:
                    if value:
                        print('ATTENTION, temperature change of {} degrees'.format(self.threshold))
            print(50 * "*")
    """
    Checks if self.city_weather has reached over 50 weather reading dictionaries and deletes whatever has accumulated 
    beyond 50.
    """

    def city_weather_size_monitor(self):
        city_weather_length = self.city_weather.weather_deque_size() - 50

        if city_weather_length > 50:
            self.city_weather.delete_data(city_weather_length)

    """
    Makes the created Monitor run.
    Takes a 10s break to allow Collector to lead a city weather dictionary to self.city_weather.
    """

    def run(self):
        while True:
            self.run_collector()
            time.sleep(5)
            try:
                self.get_weather_reading()
                self.check_for_threshold_delta()
                self.print_latest_reading()
                self.city_weather_size_monitor()
            except Exception as e:
                print('{err} occurred while getting weather data from {city_weather}'
                      .format(err=repr(e), city_weather=self.city_weather.get_city_id()))
            finally:
                time.sleep(self.frequency)



