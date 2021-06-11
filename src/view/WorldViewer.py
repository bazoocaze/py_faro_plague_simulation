from src.Force import Force
from src.calc.Point import Point
from src.simulation.World import World


class WorldViewer:
    def __init__(self, surface):
        self._surface = surface

    def process(self, context):
        pass

    def draw(self, context):
        world: World = context.world

        for y in range(world.height()):
            for x in range(world.width()):
                cel = world.cel(Point(x, y))
                if cel.has_units():
                    color = self._color_for_units(cel.units())
                    self._surface.put(x, y, color)
                else:
                    self._surface.put(x, y, (127, 192, 127))

        self._surface.draw(context)

    def _color_for_units(self, units):
        for unit in units:
            if not unit.is_destroyed():
                return self._color_for_force(unit.force(), unit)
        return 0x888888

    def _color_for_force(self, force: Force, unit):
        if force is None:
            return 0x00FFFF
        return force.color_for_unit(unit)
