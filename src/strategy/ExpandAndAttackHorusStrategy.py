from src.Force import Force
from src.simulation.SimulationContext import SimulationContext
from src.simulation.World import World

_WAIT_STEPS_TO_ATTACK = 200
_ATTACKING = "attacking"
_EXPANDING = "expanding"


class ExpandAndAttackHorusStrategy:
    def __init__(self, force: Force):
        self._force = force
        self._wait_timer = 0
        self._priority_target = None
        self._world: World = None
        self._priority_target = None
        self._current_state = _EXPANDING

    def process(self, context: SimulationContext):
        self._world = context.world
        self._wait_timer += 1
        if self._wait_timer >= _WAIT_STEPS_TO_ATTACK:
            self._wait_timer = 0
            self._rethink_strategy(context)
        else:
            if self._current_state == _ATTACKING \
                    and self._priority_target is not None \
                    and self._priority_target.is_destroyed():
                target = self._try_select_priority_target(context)
                self._force.set_priority_target(target)

    def _rethink_strategy(self, context):
        if self._current_state == _ATTACKING:
            self._current_state = _EXPANDING
            self._force.clear_priority_target()
        else:
            self._current_state = _ATTACKING
            target = self._try_select_priority_target(context)
            self._force.set_priority_target(target)

    def _try_select_priority_target(self, context):
        if self._priority_target is not None and not self._priority_target.is_destroyed():
            return self._priority_target
        self._priority_target = self._select_priority_target(context)
        return self._priority_target

    def _select_priority_target(self, context):
        return context.world \
            .unit_selector() \
            .all_enemies_of(force=self._force) \
            .of_type("Horus") \
            .random() \
            .or_else(None)
