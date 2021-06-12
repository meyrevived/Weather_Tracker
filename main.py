"""
Main script.
Prints a lovely "welcome" message.
Takes the configuration file path from CLI and gives it to the Manager, takes the api key for OpenWeather and creates an
 ApiKey from it.
"""
import sys
import threading

from Manager import Manager
from Utilities import StopRun, ApiKey

if __name__ == '__main__':
    print(50 * "X")
    print("XXXXXX     Welcome to Weather Tracker!!     XXXXXX")
    print("XXXXXX   To stop Weather Tracker, press q   XXXXXX")
    print(50 * "X")
    print()

    stop = StopRun(False)
    run_api_key = ApiKey(sys.argv[2])

    if not run_api_key.get_api_key():
        stop.say_goodbye()
        exit()

    manager = Manager()
    manager.employ_manager(sys.argv[1], run_api_key)
    producer = threading.Thread(target=manager.producer_function, args=(stop,))
    consumer = threading.Thread(target=manager.consumer_function, args=(stop,))
    producer.start()
    consumer.start()

    while not stop.stop_all and not stop.said_goodbye:
        do_stop = input().lower()
        if do_stop == 'q':
            stop.stop_all = True
            stop.say_goodbye()
            exit()
        else:
            pass

