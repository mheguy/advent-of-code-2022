from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from advent_of_code.shared_lib.utils import get_input_file_lines

TreeGrid: list[list[Tree]]


class Side(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


@dataclass
class Tree:
    height: int
    visibility: bin = 0b0000

    def set_side_visible(self, side: Side) -> None:
        self.visibility = self.visibility | (1 << side.value)

    def set_side_invisible(self, side: Side) -> None:
        self.visibility = self.visibility & ~(1 << side.value)

    def is_visible(self, side: Side) -> bool:
        return self.visibility & 1 << side.value != 0


def process_row(row: list[Tree], side: Side):
    """Set visibility of a row of trees from left-to-right."""
    tallest = 0
    for idx, tree in enumerate(row):
        if idx == 0:
            tallest = tree.height
            tree.set_side_visible(side)
            continue

        if tree.height > tallest:
            tallest = tree.height
            tree.set_side_visible(side)
        else:
            tree.set_side_invisible(side)


def transpose_tree_grid(tree_grid):
    row = tree_grid[0]
    cols = []
    for i in range(len(row)):
        col = []
        for row in tree_grid:
            col.append(row[i])
        cols.append(col)
    return cols


def process_visibility(tree_grid: TreeGrid) -> None:
    for row in tree_grid:
        process_row(row, Side.WEST)
        process_row(list(reversed(row)), Side.EAST)

    cols = transpose_tree_grid(tree_grid)

    for col in cols:
        process_row(col, Side.NORTH)
        process_row(list(reversed(col)), Side.SOUTH)


def get_list_from_tree_grid(tree_grid: TreeGrid) -> list[Tree]:
    tree_list = []
    for row in tree_grid:
        tree_list.extend(row)
    return tree_list


def main():
    lines = get_input_file_lines()
    tree_grid = [[Tree(int(char)) for char in line] for line in lines]
    process_visibility(tree_grid)

    tree_list = get_list_from_tree_grid(tree_grid)

    visible_trees = [tree for tree in tree_list if tree.visibility > 0]

    print(f"{len(visible_trees)} trees visible")


if __name__ == "__main__":
    main()
