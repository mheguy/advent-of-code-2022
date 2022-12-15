import re

from advent_of_code.shared_lib.utils import get_input_file_text

CrateStack = list[str]

input_text = get_input_file_text()
setup, instructions = input_text.split("\n\n")


def initialize_columns() -> dict[str, CrateStack]:
    setup_lines = setup.split("\n")
    clean_setup_lines = [line[1::4] for line in setup_lines]
    col_headers = clean_setup_lines[-1]
    clean_setup_lines = reversed(clean_setup_lines[:-1])
    columns = {x: [] for x in col_headers}
    for line in clean_setup_lines:
        for col_num, char in enumerate(line, start=1):
            if char != " ":
                columns[str(col_num)].append(char)
    return columns


def process_instruction_line(columns, line):
    if not line:
        return
    result = re.search(r"\w+ (\d+) \w+ (\d+) \w+ (\d+)", line)
    qty_to_move, origin, destination = result.groups()
    for _ in range(int(qty_to_move)):
        columns[destination].append(columns[origin].pop())


def main():
    columns = initialize_columns()
    for line in instructions.split("\n"):
        process_instruction_line(columns, line)

    top_crates = [stack.pop() for stack in columns.values()]
    print("".join(top_crates))


if __name__ == "__main__":
    main()
