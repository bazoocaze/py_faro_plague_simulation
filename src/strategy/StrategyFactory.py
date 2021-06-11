from src.strategy.ExpandAndAttackHorusStrategy import ExpandAndAttackHorusStrategy
from src.strategy.SimpleStrategy import SimpleStrategy


class StrategyFactory:
    def create(self, force, strategy_type: str):
        if strategy_type.casefold() == "simple_strategy":
            return SimpleStrategy(force=force)
        if strategy_type.casefold() == "expand_and_attack_horus":
            return ExpandAndAttackHorusStrategy(force=force)
        raise Exception(f"Strategy type unrecognized: {strategy_type}")
