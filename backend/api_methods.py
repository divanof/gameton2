import os
import json
from datetime import datetime
import requests
from dotenv import load_dotenv


load_dotenv()

MAIN_URL = os.environ.get("PROD_GAME_SERVER_URL")
TEST_URL = os.environ.get("TEST_GAME_SERVER_URL")
TOKEN = os.environ.get("TOKEN")
TIMEOUT = os.environ.get("GAME_SERVER_TIMEOUT")


def save_json_decorator(method_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(f"logs/{datetime.now()}_{method_name}.json", "w") as f:
                json.dump(result, f)
            return result

        return wrapper

    return decorator


def get_url(test):
    return TEST_URL if test else MAIN_URL


@save_json_decorator(method_name="play")
def play(payload, test=True):
    """Команды на построение и атаку - один раз за ход"""
    url = get_url(test)

    response = requests.post(
        f"{url}/play/zombidef/command",
        json=payload,
        headers={"X-Auth-Token": TOKEN},
        timeout=TIMEOUT,
    )
    print(response.status_code)
    return response.json()


@save_json_decorator(method_name="participate")
def participate(test=True):
    """Принять участие в игре - один раз за раунд"""
    url = get_url(test)

    response = requests.put(
        f"{url}/play/zombidef/participate",
        headers={"X-Auth-Token": TOKEN},
        timeout=TIMEOUT,
    )
    print(response.status_code)
    return response.json()


@save_json_decorator(method_name="units")
def get_units(test=True):
    """Получение всех юнитов на карте - зомби, игроки, ..."""
    url = get_url(test)

    response = requests.get(
        f"{url}/play/zombidef/units", headers={"X-Auth-Token": TOKEN}, timeout=TIMEOUT
    )
    print(response.status_code)
    return response.json()


@save_json_decorator(method_name="world")
def get_world(test=True):
    """Инфа об игровом мире"""
    url = get_url(test)

    response = requests.get(
        f"{url}/play/zombidef/world", headers={"X-Auth-Token": TOKEN}, timeout=TIMEOUT
    )
    print(response.status_code)
    return response.json()


@save_json_decorator(method_name="rounds")
def get_rounds(test=True):
    """Инфа по всем раундам (начало, конец, ...)"""
    url = get_url(test)

    response = requests.get(
        f"{url}/rounds/zombidef", headers={"X-Auth-Token": TOKEN}, timeout=TIMEOUT
    )
    print(response.status_code)
    return response.json()
