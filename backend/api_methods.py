import os
import json
from datetime import datetime
import requests
from dotenv import load_dotenv


load_dotenv()

MAIN_URL = os.environ.get('PROD_GAME_SERVER_URL',
                          'https://games.datsteam.dev/')
TEST_URL = os.environ.get('TEST_GAME_SERVER_URL',
                          'https://games-test.datsteam.dev/')
TOKEN = os.environ.get('TOKEN')
LOG_DIR = os.environ.get('LOG_DIR', 'logs')

assert TOKEN, 'token required'
os.makedirs(LOG_DIR, exist_ok=True)


def save_json_decorator(method_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = os.path.join(
                LOG_DIR, f'{timestamp}_{method_name}.json'
            )
            with open(file_path, 'w') as f:
                json.dump(result, f)
            return result
        return wrapper
    return decorator


def _request(method, endpoint, payload=None, is_test=True):
    base_url = TEST_URL if is_test else MAIN_URL

    try:
        url = f'{base_url}{endpoint}'
        headers = {'X-Auth-Token': TOKEN}
        response = requests.request(method, url, json=payload, headers=headers)
        response.raise_for_status()

        print(f'{method} {url} - Status Code: {response.status_code}')
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


@save_json_decorator(method_name="move")
def move(transports=[], is_test=True):
    """Отправка данных по коврам-самолетам для перемещения"""
    payload = {"transports": transports}
    return _request(
        'POST', '/play/magcarp/player/move', payload, is_test=is_test)


@save_json_decorator(method_name="rounds")
def get_rounds(is_test=True):
    """Получение информации о раундах"""
    return _request('GET', '/rounds/magcarp', is_test=is_test)


def _print_rounds_info(is_test=True):
    """Функция для красивого вывода информации о раундах"""
    rounds_data = get_rounds(is_test=is_test)

    game_name = rounds_data.get('gameName', 'Неизвестная игра')
    current_time = rounds_data.get('now', 'Неизвестное время')
    rounds = rounds_data['rounds']

    print(f"Информация по раундам для игры: {game_name}")
    print(f"Текущее время (UTC): {current_time}")
    print("-" * 50)

    for idx, round_info in enumerate(rounds, 1):
        round_name = round_info.get('name', 'Без названия')
        status = round_info.get('status', 'Неизвестный статус')
        start_at = round_info.get('startAt', 'Неизвестное время')
        end_at = round_info.get('endAt', 'Неизвестное время')
        duration = round_info.get('duration', 'Неизвестная длительность')

        # Преобразуем время в читабельный формат
        start_time = 'Неизвестно'
        if start_at != 'Неизвестное время':
            start_time = datetime.strptime(start_at, "%Y-%m-%dT%H:%M:%SZ")

        end_time = 'Неизвестно'
        if end_at != 'Неизвестное время':
            end_time = datetime.strptime(end_at, "%Y-%m-%dT%H:%M:%SZ")

        print(f"Раунд {idx}: {round_name}")
        print(f"  Статус: {status}")
        print(f"  Начало: {start_time}")
        print(f"  Конец: {end_time}")
        print(f"  Длительность: {duration} минут")
        print("-" * 50)
