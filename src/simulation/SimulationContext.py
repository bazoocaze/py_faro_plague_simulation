from src.simulation.World import World


class SimulationContext:
    def __init__(self, simulation, world):
        self.world: World = world
        self.simulation = simulation
        self._exit_simulation = False

    def exit_simulation(self):
        self._exit_simulation = True

    def exited(self):
        return self._exit_simulation
