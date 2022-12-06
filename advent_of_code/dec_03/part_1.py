import itertools
import string

from shared_lib.utils import get_input_file_lines


def get_priority_map() -> dict[str, int]:
    return {
        char: index
        for index, char in enumerate(
            itertools.chain(string.ascii_lowercase, string.ascii_uppercase), start=1
        )
    }


def main() -> None:
    priority_map = get_priority_map()
    lines = get_input_file_lines()

    total = 0
    for line_num, line in enumerate(lines, start=1):
        midpoint = len(line) // 2
        left = line[:midpoint]
        right = line[midpoint:]
        for char in left:
            if char in right:
                total += priority_map[char]
                break

        print(f"{line_num=} - {total=}")
        line_num += 1

    print(total)


if __name__ == "__main__":
    main()
