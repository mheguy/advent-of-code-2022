from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass, field

from shared_lib.utils import get_input_file_lines

Coordinate = namedtuple("Coordinate", "x,y")


@dataclass
class Knot:
    number: int
    x: int
    y: int
    location_tracker: set = field(default_factory=set)

    def __post_init__(self) -> None:
        self.location_tracker.add(Coordinate(0, 0))

    def move(self, movement: Coordinate) -> None:
        self.x += movement.x
        self.y += movement.y
        self.location_tracker.add(Coordinate(self.x, self.y))

    def update(self, head: Knot) -> None:
        """Compare our position to head and move as required."""
        x_diff = head.x - self.x
        y_diff = head.y - self.y

        if abs(x_diff) < 2 and abs(y_diff) < 2:
            return

        x_movement: int = 0
        y_movement: int = 0
        if x_diff > 1:
            x_movement = 1
        elif x_diff < -1:
            x_movement = -1
        elif y_diff > 1:
            y_movement = 1
        elif y_diff < -1:
            y_movement = -1

        if x_diff != 0 and y_diff != 0:
            if not x_movement:
                x_movement = -1 if x_diff < 0 else 1
            elif not y_movement:
                y_movement = -1 if y_diff < 0 else 1

        self.move(Coordinate(x_movement, y_movement))


class Rope:
    def __init__(self, num_knots: int, verbose: bool = False) -> None:
        self.knots = [Knot(i, 0, 0) for i in range(num_knots)]
        self.verbose = verbose

    @property
    def head(self) -> Knot:
        return self.knots[0]

    @property
    def tail(self) -> Knot:
        return self.knots[-1]

    def move_head(self, movement: Coordinate, dist: int) -> None:
        for _ in range(dist):
            self.head.move(movement)
            self.update_all_knots()
            self.print_knot_positions()

    def update_all_knots(self):
        for counter, knot in enumerate(self.knots[1:]):
            knot.update(self.knots[counter])

    def print_knot_positions(self):
        if self.verbose:
            for knot in self.knots:
                print(f"{knot.number}: ({knot.x},{knot.y})")


def main(num_knots: int):
    directions = {
        "U": Coordinate(0, 1),
        "D": Coordinate(0, -1),
        "R": Coordinate(1, 0),
        "L": Coordinate(-1, 0),
    }

    lines = get_input_file_lines()
    knot = Rope(num_knots)
    for line in lines:
        direction, dist_str = line.split()
        knot.move_head(directions[direction], int(dist_str))

    print(f"For {num_knots}, the last piece visited {len(knot.tail.location_tracker)} locations.")


if __name__ == "__main__":
    for value in [2, 10]:
        main(value)
