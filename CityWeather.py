"""
CityWeather object.
Contains city_id, an array of weather data dictionaries.
Has methods for returning city_id, putting data in the array, deleting data from the array, get the nth data from the
array and getting the n-1-th data from the array.
Has method for indicating when collection of weather data is too small for threshold check.
"""
from collections import deque


class CityWeather:

    def __init__(self, city_id):
        self.city_id = city_id
        self.weather_deque = deque()
        self.deque_len = 0

    """
    Returns the size of self.weather_deque.
    """
    def weather_deque_size(self):
        return len(self.weather_deque)

    """
    Puts a weather data dictionary into self.weather_deque.
    Returns True.
    """

    def put_data(self, new_weather_data):
        self.weather_deque.append(new_weather_data)
        self.deque_len += 1

    """
    Deletes one weather data dictionary from self.weather_deque.
    Returns True. 
    """

    def delete_data(self, entries_to_delete):
        try:
            for num in range(entries_to_delete):
                self.weather_deque.popleft()
            return True
        except IndexError as e:
            print('IndexError occurred when clearing {num} items from CityWeather of {city_id}'
                  .format(num=entries_to_delete, city_id=self.city_id))
            return False

    """
    Returns the last weather data dictionary that was appended to self.weather_deque.
    """

    def get_latest(self):
        if self.deque_len >= 1:
            latest_weather_dictionary = self.weather_deque[-1]
            return latest_weather_dictionary

    """
    Returns the n-1 weather data dictionary that was appended to self.weather_deque.
    """

    def get_previous(self):
        if self.deque_len >= 2:
            previous_weather_dictionary = self.weather_deque[-2]
            return previous_weather_dictionary

    """
    Returns the city_id that defines the identity of this CityWeather.
    """

    def get_city_id(self):
        safe_city_id = self.city_id
        return safe_city_id

    """
    Returns self.deque_len
    """

    def get_deque_len(self):
        safe_deque_len = self.deque_len
        return safe_deque_len
