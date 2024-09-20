from math import sqrt
import random

from api_methods import *


def get_distance(item1, item2):
    return sqrt((item1['x'] - item2['x']) ** 2 + (item1['y'] - item2['y']) ** 2)



def get_priorities(head, zombies, enemy_blocks):
    targets = []
    if zombies is None:
        return []
    enemy_blocks = enemy_blocks if enemy_blocks is not None else []
    # shuffle result
    # random.shuffle(result)
    # return result
    print(head, zombies[0])
    zombies = sorted(zombies, key=lambda d: get_distance(head, d))

    count = 25 * 2
    if enemy_blocks:
        for block in enemy_blocks:
            count -= 1
            if not count:
                break

            targets.append({
                'x': block['x'],
                'y': block['y'],
                'health': block['health']
            })

    for zombie in zombies:
        if zombie['type'] == "liner":
            targets.append({
                'x': zombie['x'],
                'y': zombie['y'],
                'health': zombie['health']
            })
            zombies.remove(zombie)

    for zombie in zombies:
        if zombie['type'] == "juggernaut" or zombie['type'] == "bomber":
            targets.append({
                'x': zombie['x'],
                'y': zombie['y'],
                'health': zombie['health']
            })
            zombies.remove(zombie)


    for zombie in zombies:
        targets.append({
            'x': zombie['x'],
            'y': zombie['y'],
            'health': zombie['health']
        })
        zombies.remove(zombie)
    return targets


def get_attack_data(units):
    """
    returns [
                {
                    "blockId": "f47ac10b-58cc-0372-8562-0e02b2c3d479",
                    "target": 
                        {
                        "x": 1,
                        "y": 1
                    }
                }
            ],
    if base should attack else None
    """
    return_data = []
    base = units["base"]
    enemy_blocks = units["enemy_blocks"] if "enemy_blocks" in units else None
    zombies = units["zombies"] if "zombies" in units else None

    head = None
    for base_elem in base:
        if 'isHead' in base_elem:
            head = base_elem
            break

    targets = get_priorities(head, zombies, enemy_blocks)

    if units['zombies'] is not None:
        for target in targets:
            for base_element in base:
                dist = 8 if 'IsHead' in base_element else 5
                if sqrt((base_element['x'] - target['x'])**2 + (base_element['y'] - target['y'])**2) <= dist and target['health'] >= 0:
                    base.remove(base_element)
                    target['health'] -= 40 if 'IsHead' in base_element else 10
                    return_data.append({
                        'blockId': base_element['id'],
                        'target': {
                            'x': target['x'], 'y': target['y']
                        }
                    })
      
    return return_data
