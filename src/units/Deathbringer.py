from src.Force import Force
from src.calc.Point import Point
from src.simulation.SimulationContext import SimulationContext
from src.units.Unit import Unit


class Deathbringer(Unit):
    def __init__(self, position: Point, force: Force = None):
        config = {
            "max_hp": 150,
            "attack_damage": 15,
            "attack_radius": 2,
            "sensor_radius": 8,
        }
        super().__init__(position, config, force)

    def process(self, context: SimulationContext):
        if self.is_destroyed():
            return

        self._world = context.world

        if self._try_offensive_response():
            return
        if self._try_chase_priority_target():
            return
        if self._try_roam():
            return
