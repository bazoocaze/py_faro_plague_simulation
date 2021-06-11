from src.calc import geometry


class UnitSelector:
    def __init__(self, world):
        self._world = world
        self._iterator = None

    def units_nearby(self, unit=None, radius=None, position=None):
        position = unit.position() if unit is not None else position
        self._iterator = self._map_cells_to_units(self._world.select_nearby(position, radius))
        if unit is not None:
            return self.not_unit(unit)
        return self

    def all_enemies_of(self, force=None, unit=None):
        self._iterator = self._filter_enemy_to(self._world.select_all_units(), force=force, unit=unit)
        return self

    def enemy_to(self, unit):
        self._iterator = self._filter_enemy_to(self._iterator, unit)
        return self

    def weakest(self):
        self._iterator = self._filter_weakest(self._iterator)
        return self

    def nearest_to(self, unit=None, position=None):
        position = unit.position() if unit is not None else position
        self._iterator = self._filter_nearest(self._iterator, position)
        return self

    def of_type(self, unit_type: str):
        self._iterator = self._filter_unit_type(self._iterator, unit_type)
        return self

    def or_else(self, default_value):
        return next(self._iterator, default_value)

    def not_unit(self, unit):
        self._iterator = self._filter_not_unit(self._iterator, unit)
        return self

    def _filter_enemy_to(self, iterator, unit=None, force=None):
        for other_unit in iterator:
            if not other_unit.is_destroyed():
                if (unit is not None and unit.is_enemy_to(other_unit)) or (
                        force is not None and force.is_enemy_to(other_unit.force())):
                    yield other_unit

    def _map_cells_to_units(self, cells_iterator):
        for cell in cells_iterator:
            for unit in cell.units():
                yield unit

    def _filter_weakest(self, unit_iterator):
        weakest = None
        for unit in unit_iterator:
            if not weakest or unit.hp() < weakest.hp():
                weakest = unit
        if weakest:
            yield weakest

    def _filter_nearest(self, unit_iterator, position):
        nearest = None
        min_distance = None
        for unit in unit_iterator:
            distance = geometry.manhattan_distance(position, unit.position())
            if not nearest or distance < min_distance:
                nearest = unit
                min_distance = distance
        if nearest:
            yield nearest

    def _filter_not_unit(self, unit_iterator, unit):
        for other_unit in unit_iterator:
            if other_unit != unit:
                yield other_unit

    def _filter_unit_type(self, unit_iterator, unit_type: str):
        for unit in unit_iterator:
            if unit.__class__.__name__.casefold() == unit_type.casefold():
                yield unit
