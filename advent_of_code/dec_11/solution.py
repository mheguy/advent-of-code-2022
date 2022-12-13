from __future__ import annotations

import math
import operator
import re
from dataclasses import dataclass
from typing import Callable

from shared_lib.utils import get_input_file_text

Item = int

operations: dict[str, Callable[[int, int], int]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
}


@dataclass
class Game:
    monkeys: dict[int, Monkey]
    worry_reduction: int = 1
    round_number: int = 0

    def __post_init__(self) -> None:
        self.common_divisor = math.prod(
            [monkey.divisor for monkey in self.monkeys.values()]
        )

    def play_rounds(self, rounds: int) -> None:
        for _ in range(rounds):
            self.play_round()

    def play_monkey_turn(self, monkey: Monkey) -> None:
        for item in monkey.items:
            item = monkey.inspect(item)
            item = item // self.worry_reduction
            item = item % self.common_divisor
            recipient = monkey.test(item)
            self.monkeys[recipient].items.append(item)
        monkey.items.clear()

    def play_round(self) -> None:
        for i in range(len(self.monkeys)):
            self.play_monkey_turn(self.monkeys[i])

        self.round_number += 1

    def transfer_item(self, monkey_id: int, item: Item) -> None:
        self.monkeys[monkey_id].items.append(item)


class Monkey:
    def __init__(self, monkey_block: str) -> None:
        self.inspection_count: int = 0
        lines = monkey_block.split("\n")

        current_str, *lines = lines
        self.id = int(re.findall(r"\d+", current_str)[0])

        current_str, *lines = lines
        self.items: list[Item] = [int(item) for item in re.findall(r"\d+", current_str)]

        current_str, *lines = lines
        _, operand, right = current_str.split(" = ")[1].split(" ")
        self.operation = operations[operand]
        self.right: int | None = None
        if right.isdigit():
            self.right = int(right)

        current_str, if_true, if_false, *lines = lines
        self.divisor: int = int(re.findall(r"\d+", current_str)[0])
        self.true_monkey = int(re.findall(r"\d+", if_true)[0])
        self.false_monkey = int(re.findall(r"\d+", if_false)[0])

    def __repr__(self) -> str:
        return f"Monkey({self.items})"

    def inspect(self, item: Item) -> Item:
        self.inspection_count += 1
        if self.right is None:
            return self.operation(item, item)
        return self.operation(item, self.right)

    def test(self, item: Item) -> int:  # sourcery skip: assign-if-exp
        if (item % self.divisor) == 0:
            return self.true_monkey
        else:
            return self.false_monkey


def parse_input(text: str) -> dict[int, Monkey]:
    monkey_blocks = text.split("\n\n")
    return {
        monkey_id: (Monkey(monkey_block))
        for monkey_id, monkey_block in enumerate(monkey_blocks)
    }


def main() -> None:
    for worry_reduction, rounds in (3, 20), (1, 10_000):
        game = Game(parse_input(get_input_file_text()), worry_reduction)
        game.play_rounds(rounds)
        inspections = sorted(
            [monkey.inspection_count for monkey in game.monkeys.values()]
        )
        solution = math.prod(inspections[-2:])
        print(f"After {rounds} rounds, the monkey business value is {solution}.")
        assert solution in [10_605, 76_728, 2_713_310_158, 21_553_910_156]


if __name__ == "__main__":
    main()
