import time
from time import sleep

from attack_logic import *
from build_logic import *
from move_logic import *
from api_methods import *


def json_read(filename: str):
    with open(filename) as f_in:
        return json.load(f_in)


def main_cycle():
    # units = json_read('logs/2024-07-13 11:05:56.598445_units.json')
    # world = json_read('logs/2024-07-13 11:05:56.857259_world.json')
    # build_data = get_build_data(units, world)
    while True:
        start_time = time.time()

        units = get_units()
        world = get_world()

        # units = json_read('logs/2024-07-13 15_28_54.940730_units.json')
        # world = json_read('logs/2024-07-13 15_28_55.213243_world.json')
        mtrx = []
        payload = {}

        attack_data = get_attack_data(units)
        # build_data = get_build_data(units, world)

        move_data = None
        move_data = get_move_data(units, mtrx)
        build_data = get_build_data(units, world, mtrx)
        # move_data = get_move_data(units, world)

        if attack_data:
            payload["attack"] = attack_data
        if build_data:
            payload["build"] = build_data
        if move_data:
            payload["moveBase"] = move_data

        print(payload)

        play(payload)

        end_time = time.time()
        elapsed_time = end_time - start_time
        remaining_sleep_time = 1.98 - elapsed_time
        if remaining_sleep_time > 0:
            print(f"Sleep for: {remaining_sleep_time}")
            sleep(remaining_sleep_time)

        else:
            print("Operation took longer than 2 seconds, no sleep added")
