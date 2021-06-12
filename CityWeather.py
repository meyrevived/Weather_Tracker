"""
CityWeather object.
Contains city_id, a deque of weather data dictionaries and the length of the weather_data deque.
Has methods for returning city_id, putting data in the deque, deleting data from the deque, get the nth data from the
deque and getting the n-1-th data from the deque.
Has method for indicating when collection of weather data is too small for threshold check.
"""
from collections import deque


class CityWeather:

    def __init__(self, city_id):
        self.city_id = city_id
        self.weather_deque = deque()
        self.deque_len = 0

    def weather_deque_size(self):
        """
        Returns the size of self.weather_deque.
        """
        return len(self.weather_deque)

    def put_data(self, new_weather_data):
        """
        Puts a weather data dictionary into self.weather_deque.
        Takes a new dictionary of weather_data
        Returns True.
        """
        self.weather_deque.append(new_weather_data)
        self.deque_len += 1

    def delete_data(self, entries_to_delete):
        """
        Deletes one weather data dictionary from self.weather_deque.
        Takes the number of entries that need to be deleted.
        Returns True.
        """
        try:
            for num in range(entries_to_delete):
                self.weather_deque.popleft()
            return True
        except IndexError as e:
            print('IndexError occurred when clearing {num} items from CityWeather of {city_id}'
                  .format(num=entries_to_delete, city_id=self.city_id))
            return False

    def get_latest(self):
        """
        Returns the last weather data dictionary that was appended to self.weather_deque.
        """
        if self.deque_len >= 1:
            latest_weather_dictionary = self.weather_deque[-1]
            return latest_weather_dictionary

    def get_previous(self):
        """
        Returns the n-1 weather data dictionary that was appended to self.weather_deque.
        """
        if self.deque_len >= 2:
            previous_weather_dictionary = self.weather_deque[-2]
            return previous_weather_dictionary

    def get_city_id(self):
        """
        Returns the city_id that defines the identity of this CityWeather.
        """
        safe_city_id = self.city_id
        return safe_city_id

    def get_deque_len(self):
        """
        Returns self.deque_len
        """
        safe_deque_len = self.deque_len
        return safe_deque_len
