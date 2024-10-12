import math
from utils import sign


# def calculate_acc_vector(trans, target_x, target_y, anomalies, consts):
#     """
#     Рассчитывает вектор движения от текущей позиции до целевой позиции.
#     Возвращает нормализованный вектор, учитывая максимальное ускорение.
#     """
#     px = 0  # power x
#     py = 0  # power y
#     for anom in anomalies:
#         d = math.hypot((anom.x - trans.x), (anom.y - trans.y))
#         if d >= anom.radius:
#             continue
        
#         a = sign(anom.strength) * anom.strength**2 / d**2
#         px += a * (trans.x - anom.x) / d
#         py += a * (trans.y - anom.y) / d
    
#     dx = target_x - trans.x
#     dy = target_y - trans.y

#     px += dx
#     py += dy

#     tp = math.hypot(px, py)  # total power
#     if tp == 0:
#         return {"x": 0, "y": 0}

#     if tp > consts.max_accel:
#         px = px * consts.max_accel / tp
#         py = py * consts.max_accel / tp

#     return {"x": px, "y": py}

# def calculate_acc_vector(trans, target_x, target_y, anomalies, consts):
#     # Вектор к цели
#     dx = target_x - trans.x
#     dy = target_y - trans.y
#     distance_to_target = math.hypot(dx, dy)

#     # Если мы уже на цели, ускорения нет
#     if distance_to_target == 0:
#         return {"x": 0, "y": 0}

#     # Инициализируем ускорение к цели
#     scale = min(consts.max_accel / distance_to_target, 1)
#     acc_x = dx * scale
#     acc_y = dy * scale

#     # Проверяем, не находимся ли мы критически близко к аномалии
#     for anomaly in anomalies:
#         dx_anomaly = anomaly.x - trans.x
#         dy_anomaly = anomaly.y - trans.y
#         distance_to_anomaly = math.hypot(dx_anomaly, dy_anomaly)

#         # Определяем критическую дистанцию (например, чуть больше радиуса аномалии)
#         critical_distance = anomaly.radius * 0.3  # Можно настроить коэффициент

#         if distance_to_anomaly <= critical_distance:
#             # Вычисляем вектор ускорения, чтобы вылететь из зоны аномалии
#             dx_away = trans.x - anomaly.x
#             dy_away = trans.y - anomaly.y
#             distance_away = math.hypot(dx_away, dy_away)

#             # Нормализуем вектор отталкивания
#             if distance_away != 0:
#                 dx_away /= distance_away
#                 dy_away /= distance_away

#                 # Ускорение максимально возможное в направлении от аномалии
#                 acc_x = dx_away * consts.max_accel
#                 acc_y = dy_away * consts.max_accel
#             else:
#                 # Если мы точно в центре аномалии (теоретически), выбираем случайное направление
#                 acc_x = consts.max_accel
#                 acc_y = 0

#             # После того как мы установили ускорение для выхода из аномалии, можем прервать цикл
#             break

#     # Проверяем, чтобы итоговый вектор ускорения не превышал максимальное значение
#     total_acceleration = math.hypot(acc_x, acc_y)
#     if total_acceleration > consts.max_accel:
#         scale = consts.max_accel / total_acceleration
#         acc_x *= scale
#         acc_y *= scale

#     return {"x": acc_x, "y": acc_y}


def calculate_acc_vector(trans, target_x, target_y, anomalies, consts):
    """
    Рассчитывает вектор движения от текущей позиции до целевой позиции.
    Возвращает нормализованный вектор, учитывая максимальное ускорение.
    """
    dx = target_x - trans.x
    dy = target_y - trans.y

    distance = math.sqrt(dx**2 + dy**2)

    if distance == 0:
        return {"x": 0, "y": 0}

    scale = min(consts.max_accel / distance, 1)
    return {"x": dx * scale, "y": dy * scale}


def уебать(trans, enemies):
    """
    Выбирает врага с наименьшим здоровьем из списка врагов.
    Возвращает координаты для атаки или None, если врагов нет.
    
    :param trans: Объект ковра-самолета (TransportCommand)
    :param enemies: Список врагов
    :return: Словарь с координатами цели или None, если врагов нет.
    """
    if trans.attack_cooldown_ms > 0:
        return None

    target_enemy = None
    for enemy in enemies:
        d = math.sqrt((trans.x - enemy.x)**2 + (trans.y - enemy.y)**2)
        if d > 200:
            continue
            
        if not target_enemy:
            target_enemy = enemy
        elif target_enemy.health > enemy.health:
            target_enemy = enemy

    return {
        'x': target_enemy.x,
        'y': target_enemy.y
    } if target_enemy else None


def get_nearest_treasure(trans, bounties):
    """Поиск ближайшей монетки к ковру"""
    x = trans.x
    y = trans.y
    min_dist = float('inf')
    min_boun = []
    for boun in bounties:
        if calculate_distance(x,y,boun.x,boun.y) < min_dist:
            min_dist = calculate_distance(x,y,boun.x,boun.y)
            min_boun = [boun.x,boun.y]

    return min_boun[0], min_boun[1]



def calculate_distance(x1, y1, x2, y2):
    """Расчет евклидова расстояния между двумя точками"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
