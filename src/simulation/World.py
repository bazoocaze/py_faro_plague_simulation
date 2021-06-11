from typing import List

from src.calc.Point import Point
from src.UnitSelector import UnitSelector


class Cel:
    def __init__(self):
        self._units = []

    @staticmethod
    def create_empty():
        return Cel()

    def add(self, unit):
        self._units.append(unit)

    def has_units(self):
        return self._units.__len__() > 0

    def units(self):
        return self._units

    def is_blocked(self):
        for unit in self._units:
            if not unit.is_destroyed():
                return True
        return False

    def remove(self, unit):
        self._units.remove(unit)

    def __repr__(self):
        if not self._units:
            return "[]"
        return "[{} units]".format(self._units.__len__())


class BlockedCel(Cel):
    def add(self, unit):
        raise Exception("Cannot add unit to blocked cel")

    def has_units(self):
        return False

    def units(self):
        return []

    def is_blocked(self):
        return True

    def remove(self, unit):
        raise Exception("Cannot remove unit from blocked cel")


class World:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._matrix: List[List[Cel]] = [[Cel.create_empty() for x in range(width)] for y in range(height)]

    def add(self, unit):
        self.cel(unit.position()).add(unit)

    def cel(self, position: Point) -> Cel:
        if self._out_of_map_range(position):
            return BlockedCel()
        return self._matrix[position.y][position.x]

    def _out_of_map_range(self, position):
        return position.x < 0 or position.x >= self.width() or position.y < 0 or position.y >= self.height()

    def height(self):
        return self._height

    def width(self):
        return self._width

    def unit_moved(self, unit, old_position, new_position):
        self.cel(old_position).remove(unit)
        self.cel(new_position).add(unit)

    def select_nearby(self, point: Point, radius: int):
        x_range = range(max(0, point.x - radius), min(self.width(), point.x + radius + 1))
        y_range = range(max(0, point.y - radius), min(self.height(), point.y + radius + 1))
        for y in y_range:
            for x in x_range:
                yield self.cel(Point(x, y))

    def select_all_units(self):
        for y in range(self._height):
            for x in range(self._width):
                cel = self._matrix[y][x]
                for unit in cel.units():
                    yield unit

    def unit_selector(self) -> UnitSelector:
        return UnitSelector(world=self)
