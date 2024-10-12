import time
import json
import math

from time import sleep
from datetime import datetime, timedelta
from random import randint

from api_methods import move, SLEEP_TIME
from extractors import parse_game_data
from models import TransportCommand
from move_logic import calculate_acc_vector


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


def _game_step(anomalies, transports, enemies, wantedList, bounties, consts):
    дывын = []
    for trans in transports:
        acceleration = calculate_acc_vector(trans, 2256, 2256, consts)

        carpet = TransportCommand(
            transport_id=trans.id,
            acceleration=acceleration,
        )

        дывын.append(carpet.to_json())

    return дывын


def main_cycle():
    result_transports = []
    is_test = True

    while True:
        _sleep_time_till_next_hour()

        start_time = time.time()

        game_data_json = move(transports=result_transports, is_test=is_test)
        if not game_data_json:
            print("=== ALARM: None in game_data_json ===")
            time.sleep(1)
            continue

        game_data = parse_game_data(data=game_data_json)

        anomalies = game_data['anomalies']
        transports = game_data['transports']
        enemies = game_data['enemies']
        wantedList = game_data['wantedList']
        bounties = game_data['bounties']
        consts = game_data['consts']

        result_transports = _game_step(anomalies, transports, enemies, wantedList, bounties, consts)

        end_time = time.time()
        elapsed_time = end_time - start_time
        remaining_sleep_time = SLEEP_TIME - elapsed_time

        print(elapsed_time, remaining_sleep_time)

        if remaining_sleep_time > 0:
            print(f"Sleep for: {remaining_sleep_time}")
            sleep(remaining_sleep_time)

        else:
            print(f"Operation took longer than {SLEEP_TIME} seconds, no sleep added")


if __name__ == '__main__':
    main_cycle()
