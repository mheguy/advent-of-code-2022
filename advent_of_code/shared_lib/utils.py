from advent_of_code.shared_lib.resources import INPUT_FOLDER


def get_input_file_lines() -> list[str]:
    input_text = get_input_file_text()
    lines = input_text.split("\n")
    return [line for line in lines if line]


def get_input_file_text() -> str:
    input_file = INPUT_FOLDER / "input.txt"
    return input_file.read_text("UTF-8")
