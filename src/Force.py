class Force:
    def __init__(self, name, color, colors):
        self._name = name
        self._color = color
        self._colors = colors
        self._priority_target = None

    def color(self):
        return self._color

    def color_for_unit(self, unit):
        unit_type = unit.__class__.__name__
        return self._colors[unit_type]

    def is_enemy_to(self, force):
        return self is not force

    def priority_target(self):
        return self._priority_target

    def has_priority_target(self):
        return self._priority_target is not None and not self._priority_target.is_destroyed()

    def clear_priority_target(self):
        self._priority_target = None

    def set_priority_target(self, target):
        self._priority_target = target
