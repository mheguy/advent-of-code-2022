from advent_of_code.dec_1.part_1 import get_elves


def get_sum_of_top_n(nums: list[int], n: int) -> int:
    total = 0
    for _ in range(n):
        current_max = max(nums)
        total += current_max
        nums.remove(current_max)

    return total


if __name__ == "__main__":
    elves = get_elves()
    print(get_sum_of_top_n(elves, 3))
