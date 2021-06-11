from src.Force import Force
from src.simulation.SimulationContext import SimulationContext
from src.simulation.World import World

_WAIT_STEPS_TO_ATTACK = 100


class ExpandAndAttackHorusStrategy:
    def __init__(self, force: Force):
        self._force = force
        self._wait_timer = 0
        self._priority_target = None
        self._world: World = None

    def process(self, context: SimulationContext):
        self._world = context.world
        self._wait_timer += 1
        if self._wait_timer >= _WAIT_STEPS_TO_ATTACK:
            self._wait_timer = 0
            if self._force.has_priority_target():
                self._force.clear_priority_target()
            else:
                target = self._select_priority_target(context)
                self._force.set_priority_target(target)

    def _select_priority_target(self, context):
        return context.world \
            .unit_selector() \
            .all_enemies_of(force=self._force) \
            .of_type("Horus") \
            .or_else(None)
