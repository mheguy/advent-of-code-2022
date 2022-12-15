"""Having done this exercise not long ago, I suspect that the next challenge will be adding 'Lizard' and 'Spock'."""

from enum import IntEnum

from advent_of_code.shared_lib.utils import get_input_file_lines


class Choice(IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3


defeat_map: dict[Choice, Choice] = {
    Choice.Rock: Choice.Scissors,
    Choice.Paper: Choice.Rock,
    Choice.Scissors: Choice.Paper,
}

choice_decryption = {"A": Choice.Rock, "B": Choice.Paper, "C": Choice.Scissors}


reverse_decryption_map: dict[Choice, list[str]] = {
    Choice.Rock: ["A", "X"],
    Choice.Paper: ["B", "Y"],
    Choice.Scissors: ["C", "Z"],
}

decryption_map: dict[str, Choice] = {}
for choice, char_list in reverse_decryption_map.items():
    for char in char_list:
        decryption_map[char] = choice


def main():
    rps_rounds = get_input_file_lines()

    total_score = 0
    row = 1
    for rps_round in rps_rounds:
        if not rps_round:
            continue

        opponent_str, player_str = rps_round.split(" ")
        opponent, player = decryption_map[opponent_str], decryption_map[player_str]
        round_score = player.value
        if player == opponent:
            round_score += 3
        elif opponent == defeat_map[player]:
            round_score += 6
        total_score += round_score
        print(f"{row} - {round_score}")
        row += 1

    print(total_score)


if __name__ == "__main__":
    main()
