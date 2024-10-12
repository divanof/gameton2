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
