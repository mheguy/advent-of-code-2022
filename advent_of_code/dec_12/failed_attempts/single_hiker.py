"""No need to complicate things with the input/matrix:
- you can compare charactes with the usual operators
- strings are just lists of chars
"""
from dataclasses import dataclass
from typing import NamedTuple

from advent_of_code.shared_lib.utils import get_input_file_lines


class Position(NamedTuple):
    x: int
    y: int


class Dimensions(NamedTuple):
    width: int
    height: int


@dataclass
class HeightMap:
    map_data: list[str]

    def __post_init__(self) -> None:
        self.cardinal_movements = ((1, 0), (-1, 0), (0, 1), (0, -1))
        self.starting_position = self._get_and_mask_special_position("S", "a")
        self.ending_position = self._get_and_mask_special_position("E", "z")
        self.dimensions = Dimensions(len(self.map_data[0]) - 1, len(self.map_data) - 1)

    def _get_and_mask_special_position(self, char: str, new_char: str) -> Position:
        """Get position for the provided char and then replace it."""
        for row_num, row in enumerate(self.map_data):
            if char in row:
                index = row.index(char)
                self.map_data[row_num] = row.replace(char, new_char)
                return Position(index, row_num)
        raise ValueError

    def get_adjacent_positions(self, pos: Position) -> list[Position]:
        """Get all valid adjacent positions we can move to."""
        map_x_limit = self.dimensions.width
        map_y_limit = self.dimensions.height
        cur_char = self.map_data[pos.y][pos.x]

        positions = []
        for x_move, y_move in self.cardinal_movements:
            new_pos = Position(pos.x + x_move, pos.y + y_move)

            # Stay in bounds
            if not (0 <= new_pos.x <= map_x_limit):
                continue
            if not (0 <= new_pos.y <= map_y_limit):
                continue

            new_height = self.map_data[new_pos.y][new_pos.x]
            if ord(new_height) - ord(cur_char) > 1:
                continue

            positions.append(new_pos)

        return positions

    def get_distance_from_position_to_target(self, position: Position) -> int:
        """Calculate the distance between a position and the end goal."""
        return abs(position.x - self.ending_position.x) + abs(
            position.y - self.ending_position.y
        )


@dataclass
class Hiker:
    """A very smart hiker.

    position: current pos
    path_history: path we are currently on
    visited_position: list of all positions previously occupied
    """

    heightmap: HeightMap

    def __post_init__(self) -> None:
        self.position = self.heightmap.starting_position
        self.path_history: list[Position] = []
        self.visited_positions: list[Position] = [self.position]

    def move_to_position(self, position: Position) -> int | None:
        print(f"Moving from {self.position} to {position}. One step closer! (Maybe?)")
        self.path_history.append(self.position)
        self.position = position

        if self.position == self.heightmap.ending_position:
            return len(self.path_history)

        self.visited_positions.append(position)
        return False

    def get_best_move(self) -> Position | None:
        """From current position, check the adjacent positions."""
        possible_moves = self.heightmap.get_adjacent_positions(self.position)
        if possible_moves := set(possible_moves) - set(self.visited_positions):
            return min(
                possible_moves, key=self.heightmap.get_distance_from_position_to_target
            )
        return None

    def undo_step(self) -> None:
        print(
            f"--- Backtracking: We have no way forward. Moving from {self.position} to {self.path_history[-1]}!!!"
        )
        self.position = self.path_history[-1]
        self.path_history.pop()


def get_number_of_steps(hiker: Hiker) -> int:
    least_steps = 0
    while True:

        if best_move := hiker.get_best_move():
            if result := hiker.move_to_position(best_move):
                if not least_steps or result < least_steps:
                    print(
                        f"Found a new shortest route: {result} steps! Previous was: {least_steps}"
                    )
                    least_steps = result
                hiker.undo_step()
                hiker.undo_step()
        else:
            hiker.undo_step()

        if (
            hiker.position == hiker.heightmap.starting_position
            and len(hiker.visited_positions) > 4
        ):
            return least_steps


def main() -> None:
    heightmap = HeightMap(get_input_file_lines())
    hiker = Hiker(heightmap)

    num_steps = get_number_of_steps(hiker)
    print(num_steps)

    # 1125 is wrong :(
    assert num_steps in [31]


if __name__ == "__main__":
    main()
