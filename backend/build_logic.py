import random

from api_methods import *

def get_near_cells(units, world, x_base, y_base):
    """
    returns [{'x': int, 'y': int}] near cells with base
    """

    # x_ds = [-1]
    # y_ds = [1]

    x_ds = [1]
    y_ds = [1]

    near_cells = []
    bases = units['base']
    random.shuffle(bases)
    for base in bases:
        x = base['x']
        y = base['y']
        # if x % 2 == 0 and y % 2 == 0:
        #     continue

        for delta_x in x_ds:
            x += delta_x
            flag = True
            for other_base in units['base']:
                if other_base['x'] == x and y == other_base['y']:
                    flag = False
            for zpot in world['zpots']:
                if zpot['x'] == x and zpot['y'] == y:
                    flag = False
            # if flag and (x % 2 != 0 or y % 2 != 0):
            if flag:
                near_cells.append({'x': x, 'y': y})
        for delta_y in y_ds:
            y += delta_y
            flag = True
            for other_base in units['base']:
                if other_base['x'] == x and y == other_base['y']:
                    flag = False
            for zpot in world['zpots']:
                if zpot['x'] == x and zpot['y'] == y:
                    flag = False
            # if flag and (x % 2 != 0 or y % 2 != 0):
            if flag:
                near_cells.append({'x': x, 'y': y})
    print('near_cells:', near_cells)
    random.shuffle(near_cells)
    return near_cells


def get_build_data(units, world, mtrx):
    """
    returns {'x': int, 'y': int} if we should build cell base else None
    """
    x_base, y_base = None, None
    for row in mtrx:
        for el in row:
            if el is None:
                continue

            if el.get('isHead', False):
                x_base, y_base = el.get('x'), el.get('y')

    print(x_base, y_base)

    return_value = []

    count = units['player']['gold']
    cur_cnt = 0

    near_cells = get_near_cells(units, world, x_base, y_base)
    return near_cells
    random.shuffle(near_cells)
    while cur_cnt < len(near_cells):
        return_value.append(near_cells[cur_cnt])
        # count -= 1
        cur_cnt += 1

    return return_value

# def get_build_data(units, world, mtrx):
#     """
#     returns {'x': int, 'y': int} if we should build cell base else None
#     """
#     return_value = []

#     count = units['player']['gold']
#     cur_cnt = 0

#     x_base, y_base = None, None
#     for row in mtrx:
#         for el in row:
#             if el is None:
#                 continue

#             if el.get('isHead', False):
#                 x_base, y_base = el.get('x'), el.get('y')

#     return return_value
