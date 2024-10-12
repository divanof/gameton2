import time
import json

from time import sleep
from datetime import datetime, timedelta

from api_methods import move
from extractors import parse_game_data


def json_read(filename: str):
    with open(filename) as f_in:
        return json.load(f_in)


def _sleep_time_till_next_hour():
    """
    Функция, которая вычисляет количество секунд до начала следующего часа.
    Используется для того, чтобы заснуть на время до окончания перерыва.
    """
    current_time = datetime.now()
    current_minute = current_time.minute

    if 55 <= current_minute < 60:
        now = datetime.now()
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        sleep_seconds = (next_hour - now).total_seconds()

        print(f"Перерыв: текущее время {current_time.strftime('%H:%M:%S')}, "
                f"ждем окончания перерыва (осталось {int(sleep_seconds)} секунд).")
        time.sleep(sleep_seconds)


def main_cycle():
    result_transports = []
    is_test = True

    while True:
        _sleep_time_till_next_hour()

        start_time = time.time()

        game_data_json = move(transports=result_transports, is_test=is_test)
        game_data = parse_game_data(data=game_data_json)

        anomalies = game_data['anomalies']
        transports = game_data['transports']
        enemies = game_data['enemies']
        wantedList = game_data['wantedList']
        bounties = game_data['bounties']
        consts = game_data['consts']

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
