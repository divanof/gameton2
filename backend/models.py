class Anomaly:
    def __init__(self, anomaly_id, x, y, radius, strength, velocity):
        self.id = anomaly_id
        self.x = x
        self.y = y
        self.radius = radius
        self.strength = strength
        self.velocity = velocity

    def __repr__(self):
        return f"Anomaly(id={self.id}, x={self.x}, y={self.y}, radius={self.radius}, strength={self.strength}, velocity={self.velocity})"


class Transport:
    def __init__(self, transport_id, x, y, velocity, health, status, attack_cooldown_ms):
        self.id = transport_id
        self.x = x
        self.y = y
        self.velocity = velocity
        self.health = health
        self.status = status
        self.attack_cooldown_ms = attack_cooldown_ms

    def __repr__(self):
        return f"Transport(id={self.id}, x={self.x}, y={self.y}, velocity={self.velocity}, health={self.health}, status={self.status})"


class Enemy:
    def __init__(self, enemy_id, x, y, health):
        self.id = enemy_id
        self.x = x
        self.y = y
        self.health = health

    def __repr__(self):
        return f"Enemy(id={self.id}, x={self.x}, y={self.y}, health={self.health})"


class Bounty:
    def __init__(self, x, y, points, radius):
        self.x = x
        self.y = y
        self.points = points
        self.radius = radius

    def __repr__(self):
        return f"Bounty(x={self.x}, y={self.y}, points={self.points}, radius={self.radius})"


class Wanted:
    def __init__(self, enemy_id, kill_bounty):
        self.id = enemy_id
        self.kill_bounty = kill_bounty

    def __repr__(self):
        return f"Wanted(id={self.id}, kill_bounty={self.kill_bounty})"


class Constants:
    def __init__(self, max_speed, max_accel, attack_range, attack_cooldown_ms, attack_damage, 
                 attack_explosion_radius, revive_timeout_sec, shield_time_ms, shield_cooldown_ms, 
                 transport_radius, map_size):
        self.max_speed = max_speed
        self.max_accel = max_accel
        self.attack_range = attack_range
        self.attack_cooldown_ms = attack_cooldown_ms
        self.attack_damage = attack_damage
        self.attack_explosion_radius = attack_explosion_radius
        self.revive_timeout_sec = revive_timeout_sec
        self.shield_time_ms = shield_time_ms
        self.shield_cooldown_ms = shield_cooldown_ms
        self.transport_radius = transport_radius
        self.map_x = map_size.get('x')
        self.map_y = map_size.get('y')

    def __repr__(self):
        return (f"Constants(max_speed={self.max_speed}, max_accel={self.max_accel}, attack_range={self.attack_range}, "
                f"attack_cooldown_ms={self.attack_cooldown_ms}, attack_damage={self.attack_damage}, "
                f"attack_explosion_radius={self.attack_explosion_radius}, revive_timeout_sec={self.revive_timeout_sec}, "
                f"shield_time_ms={self.shield_time_ms}, shield_cooldown_ms={self.shield_cooldown_ms}, "
                f"transport_radius={self.transport_radius}, map_x={self.map_x}, map_y={self.map_y})")


class TransportCommand:
    def __init__(self, transport_id, acceleration=None, activate_shield=False, attack=None):
        """
        transport_id: str - ID ковра-самолета
        acceleration: dict - словарь с ускорением {'x': value, 'y': value}
        activate_shield: bool - флаг активации щита
        attack: dict - координаты атаки {'x': value, 'y': value} (может быть None)
        """
        self.id = transport_id
        self.acceleration = acceleration or {"x": 0, "y": 0}
        self.activate_shield = activate_shield
        self.attack = attack

    def to_json(self):
        """
        Преобразует объект в JSON-формат, готовый для отправки в API.
        """
        data = {
            "id": self.id,
            "acceleration": self.acceleration,
            "activateShield": self.activate_shield
        }
        if self.attack:
            data["attack"] = self.attack
        return data

    def __repr__(self):
        return (f"TransportCommand(id={self.id}, acceleration={self.acceleration}, "
                f"activate_shield={self.activate_shield}, attack={self.attack})")
