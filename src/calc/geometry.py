from src.calc.Point import Point


def manhattan_distance(pos1, pos2):
    return abs(pos1.x - pos2.x) + abs(pos1.y + pos2.y)


def direction(from_position, to_position):
    dx = 1 if to_position.x > from_position.x else -1 if to_position.x < from_position.x else 0
    dy = 1 if to_position.y > from_position.y else -1 if to_position.y < from_position.y else 0
    return Point(dx, dy)
