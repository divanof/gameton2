import time
import json
from time import sleep

from api_methods import move
from extractors import parse_game_data


def json_read(filename: str):
    with open(filename) as f_in:
        return json.load(f_in)


def main_cycle():
    result_transports = []
    is_test = True

    while True:
        start_time = time.time()

        game_data_json = move(transports=result_transports, is_test=is_test)
        game_data = parse_game_data(data=game_data_json)

        anomalies = game_data['anomalies']
        transports = game_data['transports']
        enemies = game_data['enemies']
        wantedList = game_data['wantedList']
        bounties = game_data['bounties']

        print(len(wantedList))

        end_time = time.time()
        elapsed_time = end_time - start_time
        remaining_sleep_time = 0.32 - elapsed_time

        print(start_time, end_time, elapsed_time, remaining_sleep_time)

        if remaining_sleep_time > 0:
            print(f"Sleep for: {remaining_sleep_time}")
            sleep(remaining_sleep_time)

        else:
            print("Operation took longer than 0.33 seconds, no sleep added")


if __name__ == '__main__':
    main_cycle()
