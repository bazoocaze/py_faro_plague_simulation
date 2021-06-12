from src.Force import Force
from src.UnitFactory import UnitFactory
from src.calc.Point import Point
from src.simulation.Simulation import Simulation
from src.simulation.World import World
from src.strategy.StrategyFactory import StrategyFactory
from src.view.UI import UI
from src.view.WorldViewer import WorldViewer

CONFIG = {
    "window": {"width": 800, "height": 800},
    "world": {"width": 200, "height": 200},
    "forces": [
        {
            "name": "Plague",
            "strategy": "simple_strategy",
            # "strategy": "expand_and_attack_horus",
            "color": 0xFF0000,
            "units": [
                {"type": "Corruptor", "y": 170, "x": 171},
                {"type": "Corruptor", "y": 170, "x": 172},
                {"type": "Deathbringer", "y": 170, "x": 173},
                {"type": "Deathbringer", "y": 170, "x": 174},
                {"type": "Horus", "y": 170, "x": 170},
                {"type": "Horus", "y": 180, "x": 180},
                {"type": "Horus", "y": 180, "x": 181},
                {"type": "Horus", "y": 181, "x": 180},
                # {"type": "Horus", "y": 180, "x": 181},
                # {"type": "Horus", "y": 180, "x": 181},
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
                {"type": "Horus", "y": 40, "x": 40},
                {"type": "Horus", "y": 40, "x": 150},
                {"type": "Horus", "y": 150, "x": 40},
                # {"type": "Horus", "y": 150, "x": 45},
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
    ui = UI(width=config["window"]["width"], height=config["window"]["height"])
    world_viewer = WorldViewer(ui.world_surface(config["world"]["width"], config["world"]["height"]))
    simulation.add_entity(world_viewer)
    simulation.add_entity(ui)
    simulation.start()
    simulation.run()
    ui.terminate()


def main():
    run_simulation(CONFIG)


if __name__ == '__main__':
    main()
