from models import Anomaly, Transport, Enemy, Bounty, Wanted, Constants


def extract_anomalies(data):
    """
    Извлекает список аномалий из JSON и преобразует их в объекты класса Anomaly.
    """
    anomalies_data = data.get('anomalies', [])
    return [
        Anomaly(
            anomaly.get('id'),
            anomaly.get('x'),
            anomaly.get('y'), 
            anomaly.get('radius'),
            anomaly.get('strength'),
            anomaly.get('velocity')
        )
        for anomaly in anomalies_data
    ]


def extract_transports(data):
    """
    Извлекает список ковров-самолетов из JSON и преобразует их в объекты класса Transport.
    """
    transports_data = data.get('transports', [])
    return [
        Transport(
            transport.get('id'),
            transport.get('x'),
            transport.get('y'), 
            transport.get('velocity'),
            transport.get('health'),
            transport.get('status'),
            transport.get('attackCooldownMs')
        )
        for transport in transports_data
    ]


def extract_enemies(data):
    """
    Извлекает список врагов из JSON и преобразует их в объекты класса Enemy.
    """
    enemies_data = data.get('enemies', [])
    return [
        Enemy(
            enemy.get('id'),
            enemy.get('x'),
            enemy.get('y'),
            enemy.get('health')
        ) 
        for enemy in enemies_data
    ]


def extract_wanted_list(data):
    """
    Извлекает список 'разыскиваемых' ковров из JSON и преобразует их в объекты класса Wanted.
    """
    wanted_data = data.get('wantedList', [])
    return [
        Wanted(
            wanted.get('id'),
            wanted.get('killBounty')
        )
        for wanted in wanted_data
    ]


def extract_bounties(data):
    """
    Извлекает список наград за ковры из JSON и преобразует их в объекты класса Bounty.
    """
    bounties_data = data.get('bounties', [])
    return [
        Bounty(
            bounty.get('x'),
            bounty.get('y'),
            bounty.get('points'),
            bounty.get('radius')
        ) 
        for bounty in bounties_data
    ]


def extract_constants(data):
    """
    Извлекает константы из JSON-ответа и преобразует их в объект класса Constants.
    """
    if not data:
        return None
    return Constants(
        max_speed=data.get('maxSpeed'),
        max_accel=data.get('maxAccel'),
        attack_range=data.get('attackRange'),
        attack_cooldown_ms=data.get('attackCooldownMs'),
        attack_damage=data.get('attackDamage'),
        attack_explosion_radius=data.get('attackExplosionRadius'),
        revive_timeout_sec=data.get('reviveTimeoutSec'),
        shield_time_ms=data.get('shieldTimeMs'),
        shield_cooldown_ms=data.get('shieldCooldownMs'),
        transport_radius=data.get('transportRadius'),
        map_size=data.get('mapSize'),
    )


def parse_game_data(data):
    """
    Центральная функция для разбора JSON-ответа и выделения всех объектов.
    Возвращает словарь с массивами объектов классов.
    """
    return {
        'anomalies': extract_anomalies(data),
        'transports': extract_transports(data),
        'enemies': extract_enemies(data),
        'wantedList': extract_wanted_list(data),
        'bounties': extract_bounties(data),
        'consts': extract_constants(data),
    }
