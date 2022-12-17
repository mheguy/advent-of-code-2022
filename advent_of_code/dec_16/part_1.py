import itertools
import re
from collections import deque
from dataclasses import dataclass, field
from typing import cast

from advent_of_code.shared_lib.utils import get_input_file_lines


@dataclass
class Valve:
    name: str
    flow_rate: int
    neighbors: dict[str, int]
    flow_remaining: int = 0
    routes: dict[str, int] = field(default_factory=dict)


@dataclass
class Route:
    pos: str
    steps_taken: int


def create_map(lines: list[str]) -> dict[str, Valve]:
    valve_map = {}
    for line in lines:
        matches = cast(re.Match, re.search(r".+([A-Z]{2}).+?(\d+).+valves? (.+)", line))

        neighbors: list[str] = matches[3].split(", ")
        valve_map[matches[1]] = Valve(
            matches[1], int(matches[2]), {k: -1 for k in neighbors}
        )

    calculate_shortest_paths(valve_map)
    return valve_map


def calculate_shortest_paths(valve_map: dict[str, Valve]) -> None:
    valves_of_interest = [valve for valve in valve_map.values() if valve.flow_rate > 0]
    valves_of_interest.append(valve_map["AA"])
    # for each valve, calculate route lengths to all other valves
    for origin, target in itertools.combinations(valves_of_interest, 2):
        visited = {origin.name}
        queue = deque()
        queue.append(Route(origin.name, 0))

        while queue:
            route = queue.popleft()

            if route.pos == target.name:
                origin.routes[target.name] = route.steps_taken
                target.routes[origin.name] = route.steps_taken
                continue

            for valve_name in valve_map[route.pos].neighbors:
                if valve_name not in visited:
                    queue.append(Route(valve_name, route.steps_taken + 1))
                    visited.add(valve_name)


def main(input_filename: str) -> None:
    valve_map = create_map(get_input_file_lines(input_filename))

    timeframe = 30
    position = "AA"
    print()
    # create a tree from the input
    # have 30 time
    # no backtracking
    # start at "AA"
    # -1 to time for traversal
    # -1 to time for action
    # +N to score for action


if __name__ == "__main__":
    main("dec_16_sample.txt")
