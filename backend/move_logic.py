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
