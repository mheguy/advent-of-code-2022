from collections import defaultdict
from dataclasses import dataclass, field

from advent_of_code.shared_lib.utils import get_input_file_lines


class Display:
    def __init__(self) -> None:
        self.display_matrix: dict[int, list[str]] = defaultdict(list)

    def __repr__(self) -> str:
        return (
            "\n".join(
                [
                    "".join(self.display_matrix[i])
                    for i in range(len(self.display_matrix))
                ]
            )
            if self.display_matrix
            else "<Empty display>"
        )

    def draw_pixels(self, cycle: int, register: int) -> None:
        h_pos = (cycle - 1) % 40
        row = self.display_matrix[(cycle - 1) // 40]
        if h_pos in [max(register - 1, 0), register, min(register + 1, 39)]:
            row.append("#")
        else:
            row.append(".")


@dataclass
class CPU:
    display: Display
    cycle: int = 1
    register: int = 1
    signals: list = field(default_factory=list)
    cycle_count = {"noop": 1, "addx": 2}

    def increment_cycle(self, cycles: int) -> None:
        for _ in range(cycles):
            self.display.draw_pixels(self.cycle, self.register)
            if not (self.cycle + 20) % 40:
                self.signals.append(self.register * self.cycle)
            self.cycle += 1

    def process_command(self, command: str, value_str: str = "0") -> None:
        self.increment_cycle(self.cycle_count[command])

        if command == "addx":
            self.register += int(value_str)


def main():
    cpu = CPU(Display())
    for line in get_input_file_lines():
        cpu.process_command(*line.split())

    print(sum(cpu.signals))

    output = "\n".join(
        [
            "".join(cpu.display.display_matrix[i])
            for i in range(len(cpu.display.display_matrix))
        ]
    )
    print(output)


if __name__ == "__main__":
    main()
