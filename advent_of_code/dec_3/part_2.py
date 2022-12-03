from advent_of_code.dec_3.part_1 import get_priority_map
from shared_lib.utils import get_input_file_lines


def create_groups_of_n(list_to_split: list[str], group_size: int) -> list[list[str]]:
    num_groups = len(list_to_split) // group_size

    index = 0
    groups = []
    for _ in range(num_groups):
        groups.append(list_to_split[index:index + 3])
        index += group_size

    return groups


def find_badge(group: list[str]) -> str:
    possible_badges: dict[int, set] = {
        member_number: {item for item in member_backpack if item in group[-1]}
        for member_number, member_backpack in enumerate(group[:-1])
    }

    if badge := next(
        (bag_item for bag_item in possible_badges[0] if bag_item in possible_badges[1]),
        None,
    ):
        return badge
    else:
        raise ValueError()


def main() -> None:
    priority_map = get_priority_map()
    lines = get_input_file_lines()

    # test_input = [
    #     "vJrwpWtwJgWrhcsFMMfFFhFp",
    #     "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
    #     "PmmdzqPrVvPwwTWBwg",
    #     "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
    #     "ttgJtRGJQctTZtZT",
    #     "CrZsJsPPZsGzwwsLwLmpwMDw",
    # ]
    # lines = test_input

    groups_of_3 = create_groups_of_n(lines, 3)

    total = 0
    for group_num, group in enumerate(groups_of_3, start=1):
        badge = find_badge(group)
        total += priority_map[badge]
        print(f"{group_num=} - {badge=} - {total=}")
        group_num += 1

    print(total)


if __name__ == "__main__":
    main()
