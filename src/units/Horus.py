from src.Force import Force
from src.calc.Point import Point
from src.simulation.SimulationContext import SimulationContext
from src.simulation.World import World
from src.units.Unit import Unit


class Horus(Unit):
    def __init__(self, position: Point, force: Force = None, unit_factory=None):
        self._unit_factory = unit_factory
        config = {
            "max_hp": 300,
            "attack_damage": 25,
            "attack_radius": 3,
            "sensor_radius": 10,
        }
        super().__init__(position, config, force)
        self._production = [
            {"unit_type": "Corruptor", "quantity": 10, "cost": 5},
            {"unit_type": "Deathbringer", "quantity": 5, "cost": 15},
            {"unit_type": "Horus", "quantity": 1, "cost": 80},
        ]
        self._production_index = 0
        self._resources = 0
        self._quantity_produced = 0

    def process(self, context: SimulationContext):
        if self.is_destroyed():
            return
        self._world: World = context.world
        self._resources += 1

        if self._try_offensive_response():
            return

        if self._try_produce(context):
            return

        if self._try_roam():
            return

    def _try_produce(self, context):
        current_production = self._current_production()
        if self._resources >= current_production["cost"]:
            unit = self._produce_unit()
            context.world.add(unit)
            context.simulation.add_entity(unit)
            if self._quantity_produced >= current_production["quantity"]:
                self._start_next_production_batch()
            return True
        return False

    def _current_production(self):
        return self._production[self._production_index]

    def _produce_unit(self):
        self._resources -= self._current_production()["cost"]
        self._quantity_produced += 1
        unit_type = self._current_production()["unit_type"]
        return self._unit_factory.create(force=self.force(), unit_type=unit_type, position=self.position())

    def _start_next_production_batch(self):
        self._quantity_produced = 0
        self._production_index = (self._production_index + 1) % self._production.__len__()
