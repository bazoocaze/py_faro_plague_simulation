import time

from src.simulation.SimulationContext import SimulationContext


class Simulation:
    def __init__(self, world):
        self._world = world
        self._entities = []
        self._has_ended = False

    def add_entity(self, entity):
        self._entities.append(entity)

    def remove_entity(self, entity):
        self._entities.remove(entity)

    def start(self):
        pass

    def has_ended(self):
        return self._has_ended

    def step(self):
        context = SimulationContext(self, self._world)

        self._process_all(context)
        self._draw_all(context)

        if context.exited():
            self._has_ended = True

    def _draw_all(self, context):
        for entity in self._entities:
            if self._has_method(entity, "draw"):
                entity.draw(context)

    def _process_all(self, context):
        for entity in self._entities:
            entity.process(context)

    def run(self):
        debug_step_count = 0
        while not self.has_ended():
            time.sleep(0.25)
            self.step()

            print(".", end="")
            debug_step_count += 1
            if debug_step_count > 70:
                print("")
                debug_step_count = 0

    @staticmethod
    def _has_method(entity, method_name):
        return callable(getattr(entity, method_name, None))
