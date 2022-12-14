"""No need to complicate things with the input/matrix:
- you can compare charactes with the usual operators
- strings are just lists of chars
"""
import logging
import math
from copy import deepcopy
from dataclasses import dataclass
from typing import NamedTuple

from utils import get_input_file_lines

logging.basicConfig(
    filename="example.log", encoding="utf-8", level=logging.DEBUG, filemode="w"
)

CARDINAL_MOVEMENTS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Position(NamedTuple):
    x: int
    y: int


@dataclass
class MapPosition:
    x: int
    y: int
    height: int
    letter: str
    shortest_route: int | float = math.inf


class Dimensions(NamedTuple):
    width: int
    height: int


class HeightMap:
    def __init__(self, raw_map_data: list[str]) -> None:
        self.starting_position = self._get_and_mask_special_position(
            raw_map_data, "S", "a"
        )
        self.ending_position = self._get_and_mask_special_position(
            raw_map_data, "E", "z"
        )
        self.dimensions = Dimensions(len(raw_map_data[0]) - 1, len(raw_map_data) - 1)
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

    def process_map_data(self, raw_map_data: list[str]) -> list[list[MapPosition]]:
        heightmap_matrix = []
        for y, row in enumerate(raw_map_data):
            heightmap_row = [
                MapPosition(x, y, ord(char), char) for x, char in enumerate(row)
            ]

            heightmap_matrix.append(heightmap_row)
        return heightmap_matrix

    def get_position(self, x: int, y: int) -> MapPosition:
        # sourcery skip: assign-if-exp, reintroduce-else, swap-if-expression
        if not (0 <= x <= self.dimensions.width):
            raise ValueError
        if not (0 <= y <= self.dimensions.height):
            raise ValueError

        return self.map_data[y][x]

    def get_adjacent_positions(self, pos: Position) -> list[Position]:
        """Get all valid adjacent positions we can move to."""
        positions = []
        for x_move, y_move in CARDINAL_MOVEMENTS:
            try:
                new_pos = self.get_position(pos.x + x_move, pos.y + y_move)
            except ValueError:
                continue

            cur_pos = self.get_position(pos.x, pos.y)
            if (new_pos.height - cur_pos.height) > 1:
                continue

            positions.append(Position(new_pos.x, new_pos.y))

        return positions

    def get_distance_from_position_to_target(self, position: Position) -> int:
        """Calculate the distance between a position and the end goal."""
        return abs(position.x - self.ending_position.x) + abs(
            position.y - self.ending_position.y
        )


class Hiker:
    """A very capable hiker."""

    heightmap: HeightMap
    shortest_path: int | float = math.inf
    clone_number: int = 0

    def __init__(self, position: Position) -> None:
        self.position = position
        self._number: int = 0
        self.path_history: list[Position] = [position]

    @property
    def name(self) -> str:
        return f"Hiker {self._number}"

    def begin_journey(self) -> None:
        """Begin a journey that ends by reaching the goal (or a dead-end)."""
        while True:
            if self.position == self.heightmap.ending_position:
                steps = len(self.path_history) - 1
                if steps < Hiker.shortest_path:
                    Hiker.shortest_path = steps
                    logging.info(
                        f"{self.name} completed the journey and set a new record: {Hiker.shortest_path} moves!"
                    )
                else:
                    logging.info(
                        f"{self.name} completed the journey but didn't set a new record {steps} / {Hiker.shortest_path}."
                    )
                return

            paths = self.get_paths()
            num_moves = len(paths)

            if not num_moves:
                logging.info(f"{self.name} got stuck at {self.position}")
                return
            elif num_moves == 1 and not self.move_to_position(paths[0]):
                return
            elif num_moves > 1:
                logging.info(
                    f"{self.name} is creating {num_moves} new clones (and is retiring to live a life of luxury at {self.position})!"
                )
                for pos in paths:
                    self.send_clone_to_pos(pos)
                return

    def send_clone_to_pos(self, pos: Position) -> None:
        """Create and send a clone to the given position."""
        cloned_hiker = deepcopy(self)
        Hiker.clone_number += 1
        cloned_hiker._number = Hiker.clone_number
        if not cloned_hiker.move_to_position(pos):
            return
        cloned_hiker.begin_journey()

    def move_to_position(self, position: Position) -> bool:
        logging.info(f"{self.name} {self.position} -> {position}")
        self.position = position
        self.path_history.append(position)

        map_position = Hiker.heightmap.get_position(*position)
        if map_position.shortest_route > len(self.path_history):
            map_position.shortest_route = len(self.path_history)
            return True

        logging.info(
            f"{self.name} was on an inefficient path and stopped at {position}"
        )
        return False

    def get_paths(self) -> list[Position]:
        """From current position, check the adjacent positions."""
        possible_moves = self.heightmap.get_adjacent_positions(self.position)
        return list(set(possible_moves) - set(self.path_history))


def main() -> None:
    Hiker.heightmap = HeightMap(get_input_file_lines())
    hiker = Hiker(Hiker.heightmap.starting_position)

    hiker.begin_journey()
    logging.info(f"{Hiker.clone_number+1} hikers were killed on this endeavor.")
    logging.info(f"Shortest path was: {Hiker.shortest_path}")

    # 1125 is wrong :(
    assert Hiker.shortest_path in [31]


if __name__ == "__main__":
    main()
