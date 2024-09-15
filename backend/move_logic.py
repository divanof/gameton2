from api_methods import *
import math
import random


def get_move_data(units, mtrx):
    bx, by = mtrx[0][0]["x"], mtrx[0][0]["y"]

    points = []
    for line in mtrx:
        for objcts in line:
            if (
                objcts is not None
                and objcts["type"] is not None
                and objcts["type"] == "base"
            ):
                points.append({"x": objcts["x"], "y": objcts["y"]})

    # Инициализация переменных для хранения максимального расстояния и соответствующих координат
    max_dist = -math.inf  # Используем минус бесконечность для начала поиска
    max_coords = []

    for p in points:
        # current_max_distance = 0  # Переинициализируем максимальное расстояние для каждой точки

        # for zombie in units['zombies']:
        #     distance = abs(p['x'] - zombie['x']) + abs(p['y'] - zombie['y'])

        #     # Обновляем максимальное расстояние, если текущее расстояние больше
        #     if distance > current_max_distance:
        #         current_max_distance = distance

        # # Проверяем, обновлено ли глобальное максимальное расстояние
        # if current_max_distance > max_dist:
        #     max_dist = current_max_distance
        x, y = p["x"], p["y"]
        # if mtrx[y - by + 1][x - bx + 1]['type'] == 'base' and \
        #         mtrx[y - by - 1][x - bx - 1]['type'] == 'base' and \
        #         mtrx[y - by + 1][x - bx - 1]['type'] == 'base' and \
        #         mtrx[y - by - 1][x - bx + 1]['type'] == 'base':

        if (
            mtrx[y - by + 1][x - bx]["type"] == "base"
            and mtrx[y - by - 1][x - bx]["type"] == "base"
            and mtrx[y - by][x - bx + 1]["type"] == "base"
            and mtrx[y - by][x - bx - 1]["type"] == "base"
        ):
            good = (p["x"], p["y"])
            max_coords.append(good)

    random.shuffle(max_coords)
    max_coords = max_coords[0] if len(max_coords) > 0 else None
    if max_coords is None:
        return None
    return (
        {"x": 1, "y": 1}
        # {"x": max_coords[0], "y": max_coords[1]} if max_coords else None
    )  # {'x': points[0]['x'], 'y': points[0]['y']}

    # return {'x': int, 'y': int},{'blockId':basa['id'],'target':{'x': minxzomb, 'y': minyzomb}}
