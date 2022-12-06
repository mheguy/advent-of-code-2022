import re

from advent_of_code.dec_05.part_1 import initialize_columns
from shared_lib.utils import get_input_file_text

CrateStack = list[str]

input_text = get_input_file_text()
setup, instructions = input_text.split("\n\n")


def process_instruction_line(columns, line):
    if not line:
        return
    result = re.search(r"\w+ (\d+) \w+ (\d+) \w+ (\d+)", line)
    qty_to_move_str, origin, destination = result.groups()
    qty_to_move = int(qty_to_move_str)

    taken_crates = [columns[origin].pop() for _ in range(qty_to_move)]
    taken_crates.reverse()

    for n in range(qty_to_move):
        columns[destination].append(taken_crates[n])


def main():
    columns = initialize_columns()
    for line in instructions.split("\n"):
        process_instruction_line(columns, line)

    top_crates = [stack.pop() for stack in columns.values()]
    print("".join(top_crates))


if __name__ == "__main__":
    main()
