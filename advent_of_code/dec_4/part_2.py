# Find if set is completely contained in other
from shared_lib.utils import get_input_file_lines


def main() -> int:
    lines = get_input_file_lines()

    any_overlap = 0
    for line in lines:
        elves = line.split(",")
        assignment_sets = []
        for elf in elves:
            lower, upper = elf.split("-")
            assignment_sets.append(set(range(int(lower), int(upper)+1)))

        if assignment_sets[0].intersection(assignment_sets[1]):
            any_overlap += 1
    
    return any_overlap

if __name__ == "__main__":
    print(main())