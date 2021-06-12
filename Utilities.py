"""
A collection of small classes and functions used throughout the main code.
"""

import re


class ApiKey:
    """
    The API key for OpenWeather.
    Takes a string given to the run at cli and validates that it is indeed an API key matching what OpenWeather accepts
    in their REST call and nothing malicious or
    missing important data.
    """

    def __init__(self, key):
        correct_key = re.compile("[a-z0-9]{32}")
        if re.fullmatch(correct_key, key):
            self.key = key
        else:
            print("Bad API key, please check your contract with OpenWeather")
            self.key = None

    def get_api_key(self):
        temp_key = self.key
        return temp_key


def set_task_state_with_lock(manager, monitor, at_work):
    """
    Manages locks for the monitor threads that are raised and run.
    Takes a Manager, a Monitor and a boolean of whether the Monitor is at_work
    """
    manager.lock.acquire()
    monitor.at_work = at_work
    manager.lock.release()


class StopRun:
    """
    StopRun object. Exists for all projects.
    Is used to control whether or not Weather_Tracker runs or not.
    Is either set to True or False.
    """

    def __init__(self, stop_all):
        self.stop_all = stop_all
        self.said_goodbye = False

    def say_goodbye(self):
        """
        Single function for printing the farewell message.
        Ensures calling it will set stop_all to True is it hasn't been set so already.
        Ensures the farewell message is not printed more than once.
        """

        if not self.said_goodbye:
            print()
            print(50 * "X")
            print("XXXXXX Thank you for using Weather Tracker! XXXXXX")
            print(50 * "X")
            self.said_goodbye = True

            if not self.stop_all:
                self.stop_all = True
