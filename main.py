from src.Force import Force
from src.calc.Point import Point
from src.simulation.Simulation import Simulation
from src.view.UI import UI
from src.simulation.World import World
from src.view.WorldViewer import WorldViewer
from src.strategy.StrategyFactory import StrategyFactory
from src.UnitFactory import UnitFactory

CONFIG = {
    "window": {"width": 640, "height": 480},
    "world": {"width": 100, "height": 100},
    "forces": [
        {
            "name": "Plague",
            "strategy": "simple_strategy",
            "color": 0xFF0000,
            "units": [
                {"type": "Corruptor", "y": 70, "x": 71},
                {"type": "Corruptor", "y": 70, "x": 72},
                {"type": "Deathbringer", "y": 70, "x": 73},
                {"type": "Deathbringer", "y": 70, "x": 74},
                {"type": "Horus", "y": 70, "x": 70},
                {"type": "Horus", "y": 80, "x": 80},
                {"type": "Horus", "y": 80, "x": 81},
                {"type": "Horus", "y": 80, "x": 81},
            ],
            "colors": {
                "Corruptor": 0xFF0000,
                "Deathbringer": 0xFF7F00,
                "Horus": 0xFFFF00,
            }
        },
        {
            "name": "Earth Defence Force",
            "strategy": "expand_and_attack_horus",
            "color": 0x0000FF,
            "units": [
                {"type": "Horus", "y": 20, "x": 20},
                {"type": "Horus", "y": 20, "x": 80},
                {"type": "Horus", "y": 80, "x": 20},
            ],
            "colors": {
                "Corruptor": 0x0000FF,
                "Deathbringer": 0x007FFF,
                "Horus": 0x00FFFF,
            }
        }
    ]
}


def load(config):
    world = World(config["world"]["width"], config["world"]["height"])
    simulation = Simulation(world)
    unit_factory = UnitFactory()
    strategy_factory = StrategyFactory()
    for force_config in config["forces"]:
        force = Force(force_config["name"], force_config["color"], force_config["colors"])
        strategy = strategy_factory.create(force=force, strategy_type=force_config["strategy"])
        simulation.add_entity(strategy)
        for unit_config in force_config["units"]:
            unit = unit_factory.create(force, unit_config["type"], Point(unit_config["x"], unit_config["y"]))
            world.add(unit)
            simulation.add_entity(unit)
    return simulation


def run_simulation(config):
    simulation = load(config)
    ui = UI()
    world_viewer = WorldViewer(ui.world_surface())
    simulation.add_entity(world_viewer)
    simulation.add_entity(ui)
    simulation.start()
    simulation.run()
    ui.terminate()


def main():
    run_simulation(CONFIG)


if __name__ == '__main__':
    main()
