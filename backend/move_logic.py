import math
from utils import sign


def calculate_acc_vector(trans, target_x, target_y, anomalies, consts):
    """
    Рассчитывает вектор движения от текущей позиции до целевой позиции.
    Возвращает нормализованный вектор, учитывая максимальное ускорение.
    """
    px = 0  # power x
    py = 0  # power y
    for anom in anomalies:
        d = math.hypot((anom.x - trans.x), (anom.y - trans.y))
        if d >= anom.radius:
            continue
        
        a = sign(anom.strength) * anom.strength**2 / d**2
        px += a * (trans.x - anom.x) / d
        py += a * (trans.y - anom.y) / d
    
    dx = target_x - trans.x
    dy = target_y - trans.y

    px += dx
    py += dy

    tp = math.hypot(px, py)  # total power
    if tp == 0:
        return {"x": 0, "y": 0}

    if tp > consts.max_accel:
        px = px * consts.max_accel / tp
        py = py * consts.max_accel / tp

    return {"x": px, "y": py}


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
