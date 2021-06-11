from src.units.Corruptor import Corruptor
from src.units.Deathbringer import Deathbringer
from src.units.Horus import Horus


class UnitFactory:
    def create(self, force, unit_type: str, position):
        if unit_type.casefold() == "corruptor".casefold():
            return Corruptor(force=force, position=position)
        if unit_type.casefold() == "deathbringer".casefold():
            return Deathbringer(force=force, position=position)
        if unit_type.casefold() == "horus".casefold():
            return Horus(force=force, position=position, unit_factory=self)
        raise Exception(f"Unknown unit type: {unit_type}")
