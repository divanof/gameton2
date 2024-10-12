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
    def __init__(self, transport_id, x, y, velocity, health, status):
        self.id = transport_id
        self.x = x
        self.y = y
        self.velocity = velocity
        self.health = health
        self.status = status

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
