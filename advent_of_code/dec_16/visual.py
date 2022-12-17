import graphviz

from advent_of_code.dec_16.part_1 import Valve, create_map
from advent_of_code.shared_lib.resources import INPUT_FOLDER
from advent_of_code.shared_lib.utils import get_input_file_lines


def create_neighbors_graph(valve_map) -> None:
    dot = graphviz.Graph(
        "dec_16_raw", comment="AOC Dec 16", directory=INPUT_FOLDER, format="png"
    )
    edges = set()
    for name, valve in valve_map.items():
        dot.node(name, label=f"{name} - {valve.flow_rate}")
        for neighbor in valve.neighbors:
            edges.add(tuple(sorted([name, neighbor])))

    dot.edges(edges)
    dot.render(view=True)


def create_routes_graph(valve_map: dict[str, Valve]) -> None:
    dot = graphviz.Graph(
        "dec_16_abbreviated", comment="AOC Dec 16", directory=INPUT_FOLDER, format="png"
    )
    edges = set()
    for name, valve in valve_map.items():
        if not valve.routes:
            continue

        dot.node(name, label=f"{name} - {valve.flow_rate}")
        for route_end, length in valve.routes.items():
            edges.add((*sorted([name, route_end]), length))

    for head, tail, length in edges:
        dot.edge(tail, head, str(length))
    dot.render(view=True)


def main(input_filename: str) -> None:
    valve_map = create_map(get_input_file_lines(input_filename))

    # create_neighbors_graph(valve_map)
    create_routes_graph(valve_map)


if __name__ == "__main__":
    main("dec_16_sample.txt")
