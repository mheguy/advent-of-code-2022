from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass, field
from typing import Generator

from advent_of_code.shared_lib.classes import Position
from advent_of_code.shared_lib.utils import get_input_file_lines

CARDINAL_MOVEMENTS = ((1, 0), (-1, 0), (0, 1), (0, -1))


@dataclass
class Journey:
    pos: Position
    steps_taken: int


MapDict = dict[Position, str]


class HeightMap:
    def __init__(self, raw_map_data: list[str]) -> None:
        self.starting_position = self._get_and_mask_special_position(
            raw_map_data, "S", "a"
        )
        self.ending_position = self._get_and_mask_special_position(
            raw_map_data, "E", "z"
        )
        self.x_max = len(raw_map_data[0]) - 1
        self.y_max = len(raw_map_data) - 1
        self.map_data = self.process_map_data(raw_map_data)

    @staticmethod
    def _get_and_mask_special_position(
        raw_map_data: list[str], char: str, new_char: str
    ) -> Position:
        """Get position for the provided char and then replace it."""
        for row_num, row in enumerate(raw_map_data):
            if char in row:
                index = row.index(char)
                raw_map_data[row_num] = row.replace(char, new_char)
                return Position(index, row_num)
        raise ValueError

    def process_map_data(self, raw_map_data: list[str]) -> MapDict:
        map_data = {}
        for y, row in enumerate(raw_map_data):
            for x, char in enumerate(row):
                map_data[Position(x, y)] = char

        return map_data

    def get_position(self, x: int, y: int) -> Position:
        if not (0 <= x <= self.x_max):
            raise ValueError
        if not (0 <= y <= self.y_max):
            raise ValueError

        return Position(x, y)

    def get_adjacent_positions(self, pos: Position) -> list[Position]:
        """Get all valid adjacent positions we can move to."""
        positions = []
        for x_move, y_move in CARDINAL_MOVEMENTS:
            try:
                new_pos = self.get_position(pos.x + x_move, pos.y + y_move)
            except ValueError:
                continue

            cur_pos = self.get_position(pos.x, pos.y)
            if (ord(self.map_data[new_pos]) - ord(self.map_data[cur_pos])) > 1:
                continue

            positions.append(Position(new_pos.x, new_pos.y))

        return positions

    def get_departure_points(self) -> Generator[Position, None, None]:
        all_departure_points = (
            pos for pos, char in self.map_data.items() if char == "a"
        )

        for departure_point in all_departure_points:
            adjacents = self.get_adjacent_positions(departure_point)
            if not adjacents:
                continue

            point_char = self.map_data[departure_point]
            surrounded_by_losers = all(
                point_char == self.map_data[adjacent] for adjacent in adjacents
            )

            if not surrounded_by_losers:
                yield departure_point


@dataclass
class Hiker:
    """A hiker with an eidetic memory.

    Will try as many paths as needed to finds the shortest path to the goal.
    """

    position: Position
    heightmap: HeightMap
    positions_visited: set[Position] = field(default_factory=set)
    queue: deque[Journey] = field(default_factory=deque)

    def explore_paths(self) -> int | float:
        """Begin a long series of trial and error journeys."""
        self.queue.append(Journey(self.position, 0))
        while self.queue:
            cur_journey = self.queue.popleft()
            self.position = cur_journey.pos

            if self.position == self.heightmap.ending_position:
                return cur_journey.steps_taken

            paths = self.get_paths_for_investigation()
            self.positions_visited = paths | self.positions_visited
            for path in paths:
                self.queue.append(Journey(path, cur_journey.steps_taken + 1))

        return math.inf

    def get_paths_for_investigation(self) -> set[Position]:
        """From current position, get all viable paths forward."""
        possible_paths = self.heightmap.get_adjacent_positions(self.position)
        return set(possible_paths) - self.positions_visited


def main() -> None:
    heightmap = HeightMap(get_input_file_lines())
    hiker = Hiker(heightmap.starting_position, heightmap)

    steps_from_fixed_start = hiker.explore_paths()
    print(f"Shortest path from fixed start is: {steps_from_fixed_start}")

    assert steps_from_fixed_start in [31, 423]

    steps_in_shortest_path = min(
        Hiker(start, heightmap).explore_paths()
        for start in heightmap.get_departure_points()
    )
    print(f"Shortest single path is: {steps_in_shortest_path}")

    assert steps_in_shortest_path in [29, 416]


if __name__ == "__main__":
    main()
