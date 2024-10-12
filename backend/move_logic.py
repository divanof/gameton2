import math


def calculate_acc_vector(trans, target_x, target_y, consts):
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
