"""
Manager object.
Parses configuration JSON into internal variables.
Creates CityWeather objects according to configurations in configuration JSON.
Creates Monitors per CityWeather.
Has producer function which creates one run job per Monitor and sets them running if the time has come for them to
run according to the frequency detailed in the configuration JSON.
Has consumer function for timely terminating the Monitors' run jobs.
"""
import json
import time
from datetime import datetime, timezone
import threading

from CityWeather import CityWeather
from Monitor import Monitor
from Utilities import set_task_state_with_lock


class Manager:

    def __init__(self):
        self.lock = threading.Lock()
        self.pool_size = 5
        self.weather_config_json = []
        self.monitors = []
        self.jobs_queue = []

    def configuration_parser(self, configuration_file):
        """
        Parses each dictionary in the configuration JSON and loads its values to city_id, city_name, frequency and
        threshold.
        Fetches the configuration JSON from the file system.
        Takes each configuration section in the JSON file and turns it into a dictionary with the same data in the list
        configuration_json.
        Returns configuration_json.
        """
        try:
            with open(configuration_file, 'r') as config_json:
                config_data = json.load(config_json)
                for item in config_data:
                    item = {"city_id": item["city_id"], "city_name": item["city_name"],
                            "frequency": item["frequency"], "threshold": item["threshold"]}
                    self.weather_config_json.append(item)
        except IOError as e:
            print('{err} occurred when opening {f}'.format(err=repr(e), f=configuration_file))
            return False

    def producer_function(self, stop):
        """
        Producer function for making Monitors and to start running if it's time for them to run, and adding their thread
        to jobs_queue.
        Takes a Stop.
        """
        while not stop.stop_all:
            now_utc = datetime.now(timezone.utc)

            for monitor in self.monitors:
                delta_time = (now_utc - monitor.last_run_at).seconds
                if not monitor.at_work and delta_time > monitor.frequency and len(self.jobs_queue) < self.pool_size:
                    set_task_state_with_lock(self, monitor, True)
                    job = threading.Thread(target=monitor.run_monitor, args=(stop, self))
                    job.start()
                    self.jobs_queue.append(job)

            time.sleep(1)
        else:
            stop.say_goodbye()
            exit()

    def consumer_function(self, stop):
        """
        Consumer function for going over the the jobs of running Monitors and bringing them to a stop one by one.
        Runs until stop.stop_all is set to True.
        Takes a Stop.
        """
        while not stop.stop_all:
            for job in self.jobs_queue:
                job.join()
                self.jobs_queue.remove(job)
            time.sleep(1)
        else:
            stop.say_goodbye()
            exit()

    def employ_manager(self, config_file_path, run_api_key):
        """
        Runs the Manager functionality.
        Checks that loading the configuration JSON was successful.
        Creates a Monitor and a CityWeather according the data in each dictionary in configuration_parser's returned
        configuration_json.
        Sets each created Monitor running.
        Takes the name of the configuration JSON and an ApiKey.
        """

        self.configuration_parser(config_file_path)

        if self.weather_config_json:
            for config_dict in self.weather_config_json:
                city_weather = CityWeather(config_dict["city_id"])
                monitor = Monitor(config_dict["frequency"], config_dict["threshold"], city_weather, run_api_key)
                self.monitors.append(monitor)
