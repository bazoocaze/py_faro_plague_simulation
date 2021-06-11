import random

from src.calc import geometry
from src.Force import Force
from src.calc.Point import Point
from src.simulation.SimulationContext import SimulationContext
from src.simulation.World import World


class Unit:
    def __init__(self, position: Point, config: dict, force: Force = None):
        self._force = force
        self._position = position
        self._world: World = None
        self._name = "{}{}".format(self.__class__.__name__, random.randint(0, 1000))
        self._config = config
        self._hp = self._max_hp()

    def __str__(self):
        return self._name

    def __repr__(self):
        return "{}[force={}, pos={}]".format(self.__class__.__name__, self._force, self._position)

    def position(self):
        return self._position

    def force(self):
        return self._force

    def hp(self):
        return self._hp

    def process(self, context: SimulationContext):
        pass

    def move_to(self, new_position):
        # print(f"UNIT: {self} moving to {new_position}")
        old_position = self._position
        self._position = new_position
        self._world.unit_moved(self, old_position, new_position)

    def attack(self, enemy):
        print(f"UNIT: {self} attack {enemy}")
        enemy.take_damage(self._attack_damage())

    def take_damage(self, damage):
        print(f"UNIT: {self} takes {damage} damage")
        if self.is_destroyed():
            print(f"UNIT: {self} is already destroyed")
            return
        self._hp -= damage
        if self.is_destroyed():
            print(f"UNIT: {self} is destroyed")

    def is_destroyed(self):
        return self._hp <= 0

    def _try_offensive_response(self):
        return self._try_attack() or self._try_chase()

    def _try_attack(self):
        enemy = self._world.unit_selector() \
            .units_nearby(unit=self, radius=self._attack_radius()) \
            .enemy_to(self) \
            .weakest() \
            .or_else(None)

        if enemy:
            self.attack(enemy)
        return enemy is not None

    def _try_chase(self):
        enemy = self._world.unit_selector() \
            .units_nearby(unit=self, radius=self._sensor_radius()) \
            .enemy_to(self) \
            .nearest_to(unit=self).or_else(None)

        if enemy:
            # print(f"UNIT: {self} chasing {enemy}")
            direction = geometry.direction(self._position, enemy.position())
            new_position = Point(self._position.x + direction.x, self._position.y + direction.y)
            return self._try_move_to(new_position)
        return False

    def _try_chase_priority_target(self):
        if self.force().has_priority_target():
            enemy = self.force().priority_target()
            direction = geometry.direction(self._position, enemy.position())
            new_position = Point(self._position.x + direction.x, self._position.y + direction.y)
            return self._try_move_to(new_position)
        return False

    def _try_roam(self):
        dx = random.randint(0, 2)
        dy = random.randint(0, 2)
        new_position = Point(self._position.x + dx - 1, self._position.y + dy - 1)
        return new_position != self._position and self._try_move_to(new_position)

    def _try_move_to(self, new_position):
        if not self._world.cel(new_position).is_blocked():
            self.move_to(new_position)
            return True
        # print(f"UNIT: {self} cannot move to {new_position}")
        return False

    def is_enemy_to(self, unit):
        return self._independent_unit() or self._force_is_enemy_to(unit)

    def _force_is_enemy_to(self, unit):
        return self._force.is_enemy_to(unit.force())

    def _independent_unit(self):
        return self._force is None

    def _max_hp(self):
        return self._config["max_hp"]

    def _attack_radius(self):
        return self._config["attack_radius"]

    def _attack_damage(self):
        return self._config["attack_damage"]

    def _sensor_radius(self):
        return self._config["sensor_radius"]
