from typing import NamedTuple

from advent_of_code.shared_lib.utils import get_input_file_lines


class Position(NamedTuple):
    x: int
    y: int


def main(target_y_level: int, input_filename: str) -> None:
    lines = get_input_file_lines(input_filename)
    scanned_tiles_at_level = set()
    for line in lines:
        sensor, beacon = list(
            map(
                eval,
                map(
                    lambda x: f"Position({x})",
                    line.replace("Sensor at ", "").split(": closest beacon is at "),
                ),
            )
        )
        radius = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)
        upper_limit = sensor.y + radius
        lower_limit = sensor.y - radius

        if not (lower_limit <= target_y_level <= upper_limit):
            continue

        # because we are within the radius, we calculate which squares we scan
        distance_from_target_level = abs(sensor.y - target_y_level)
        radius_at_target = radius - distance_from_target_level

        for x in range(sensor.x - radius_at_target, sensor.x + radius_at_target + 1):
            scanned_tiles_at_level.add(Position(x, target_y_level))

        if beacon in scanned_tiles_at_level:
            scanned_tiles_at_level.remove(beacon)

    part_1_score = len(scanned_tiles_at_level)

    print(part_1_score)
    if target_y_level == 10:
        assert part_1_score == 26
    else:
        assert part_1_score == 4951427


if __name__ == "__main__":
    main(10, "dec_15_sample.txt")  # test data
    main(2_000_000, "dec_15_real.txt")  # real data
