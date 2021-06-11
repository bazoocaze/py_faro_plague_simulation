from src.simulation.SimulationContext import SimulationContext


class SimpleStrategy:
    def __init__(self, force):
        self._force = force

    def process(self, context: SimulationContext):
        # no extra strategy for force
        pass
