from enum import Enum
from itertools import pairwise
from typing import NamedTuple

from advent_of_code.shared_lib.utils import get_input_file_lines

Grid = dict["Position", "Material"]


class Position(NamedTuple):
    x: int
    y: int


class Material(Enum):
    AIR = 0
    ROCK = 1
    SAND = 2


def draw_grid_lines(grid: Grid, positions: list[Position]) -> Grid:
    for pos1, pos2 in pairwise(positions):
        x1, x2 = sorted([pos1.x, pos2.x])
        y1, y2 = sorted([pos1.y, pos2.y])
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                grid[Position(x, y)] = Material.ROCK

    return grid


def create_base_grid(positions: list[Position], has_floor: bool) -> Grid:
    # sourcery skip: dict-comprehension, use-itertools-product
    """Create an empty grid."""
    x_values = []
    y_values = []
    for pos in positions:
        x_values.append(pos.x)
        y_values.append(pos.y)

    x_values.sort()
    y_values.sort()

    y_min = 0
    y_max = y_values[-1] + 2
    x_min = x_values[0] - y_max
    x_max = x_values[-1] + y_max

    grid = {}
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            grid[Position(x, y)] = Material.AIR

    if has_floor:
        for x in range(x_min, x_max + 1):
            grid[Position(x, y_max)] = Material.ROCK

    return grid


def create_grid(lines: list[str], has_floor: bool = False) -> Grid:
    grid_walls: Grid = {}
    all_positions: list[Position] = []
    for line in lines:
        str_positions = line.split(" -> ")

        positions = []
        for str_pos in str_positions:
            x, y = str_pos.split(",")
            positions.append(Position(int(x), int(y)))

        all_positions.extend(positions)
        draw_grid_lines(grid_walls, positions)

    base_grid = create_base_grid(all_positions, has_floor)

    return base_grid | grid_walls


def drop_sand_grains(grid: Grid) -> Grid:
    while True:
        if pos := drop_sand_grain(grid):
            grid[pos] = Material.SAND
        else:
            return grid


def drop_sand_grain(grid: Grid) -> Position | None:
    """Determine a new sand grain's final position."""
    starting_pos = Position(500, 0)
    pos = starting_pos

    while True:
        new_y = pos.y + 1
        down = Position(pos.x, new_y)
        down_left = Position(pos.x - 1, new_y)
        down_right = Position(pos.x + 1, new_y)

        if down not in grid:
            return None
        if grid[down] is Material.AIR:
            pos = down
            continue

        if down_left not in grid:
            return None
        if grid[down_left] is Material.AIR:
            pos = down_left
            continue

        if down_right not in grid:
            return None
        if grid[down_right] is Material.AIR:
            pos = down_right
            continue

        break

    return None if pos == starting_pos else pos


def main() -> None:
    input_lines = get_input_file_lines()

    grid = create_grid(input_lines)
    grid = drop_sand_grains(grid)
    sand_grains = sum(material is Material.SAND for material in grid.values())
    print(f"{sand_grains} grains of sand are now in the grid (no floor).")
    assert sand_grains in [24, 817]

    grid = create_grid(input_lines, True)
    grid = drop_sand_grains(grid)
    sand_grains = sum(material is Material.SAND for material in grid.values()) + 1
    print(f"{sand_grains} grains of sand are now in the grid (with floor).")
    assert sand_grains in [93, 23_416]


if __name__ == "__main__":
    main()
