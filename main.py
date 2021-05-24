"""
Main script.
Prints a lovely "welcome" message.
Takes the configuration file path from CLI and gives it to the Manager.
"""
import sys
from Manager import run_manager

if __name__ == '__main__':
    print(41 * "X")
    print("XXXXXX Welcome to Weather Tracker! XXXXXX")
    print(41 * "X")
    print()

    try:
        run_manager(sys.argv[1])
    except KeyboardInterrupt:
        print()
        print(49 * "X")
        print("XXXXXX Thank you for using Weather Tracker! XXXXXX")
        print(49 * "X")
        exit()

