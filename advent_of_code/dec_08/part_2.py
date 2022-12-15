from __future__ import annotations

import math
from dataclasses import dataclass, field

from advent_of_code.dec_08.part_1 import get_list_from_tree_grid, transpose_tree_grid
from advent_of_code.shared_lib.utils import get_input_file_lines

TreeGrid: list[list[Tree]]


@dataclass
class Tree:
    height: int
    views: list = field(default_factory=list)

    @property
    def score(self) -> int:
        return math.prod(self.views)

    def add_view(self, distance: int) -> None:
        self.views.append(distance)


def process_row_view_distances(row: list[Tree]):
    """Set view distances of a row of trees looking right to left."""
    for idx, tree in enumerate(row):
        view_distance = 0

        for i in range(idx - 1, -1, -1):
            view_distance += 1
            if tree.height <= row[i].height:
                break

        tree.add_view(view_distance)


def process_view_distances(tree_grid: TreeGrid) -> None:
    for row in tree_grid:
        process_row_view_distances(row)
        process_row_view_distances(list(reversed(row)))

    cols = transpose_tree_grid(tree_grid)

    for col in cols:
        process_row_view_distances(col)
        process_row_view_distances(list(reversed(col)))


def main():
    lines = get_input_file_lines()
    tree_grid = [[Tree(int(char)) for char in line] for line in lines]
    process_view_distances(tree_grid)

    tree_list = get_list_from_tree_grid(tree_grid)

    best_view = max(tree_list, key=lambda x: x.score)

    print(f"{best_view.score} trees visible")


if __name__ == "__main__":
    main()
