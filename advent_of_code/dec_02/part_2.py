from enum import IntEnum

from advent_of_code.dec_2.part_1 import Choice
from advent_of_code.dec_2.part_1 import decryption_map as p1_decryption_map
from advent_of_code.dec_2.part_1 import defeat_map
from advent_of_code.shared_lib.utils import get_input_file_lines


class Outcome(IntEnum):
    Win = 6
    Lose = 0
    Draw = 3


reverse_defeat_map = {v: k for k, v in defeat_map.items()}

decryption_map: dict[str, Choice | Outcome] = p1_decryption_map.copy()
decryption_map["X"] = Outcome.Lose
decryption_map["Y"] = Outcome.Draw
decryption_map["Z"] = Outcome.Win


def main():
    rps_rounds = get_input_file_lines()

    # test_rounds = ["A Y", "B X", "C Z"]
    # rps_rounds = test_rounds

    total_score = 0
    row = 1
    for rps_round in rps_rounds:
        if not rps_round:
            continue

        opponent_str, player_str = rps_round.split(" ")
        opponent, round_outcome = (
            decryption_map[opponent_str],
            decryption_map[player_str],
        )
        round_score = round_outcome.value
        if round_outcome == Outcome.Win:
            player_choice = reverse_defeat_map[opponent]
        elif round_outcome == Outcome.Lose:
            player_choice = defeat_map[opponent]
        elif round_outcome == Outcome.Draw:
            player_choice = opponent
        else:
            raise ValueError()

        round_score += player_choice.value
        total_score += round_score
        print(f"{row} - {round_score} - {opponent} v {player_choice}")
        row += 1

    print(total_score)


if __name__ == "__main__":
    main()
