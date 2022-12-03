from shared_lib.resources import INPUT_FOLDER


def get_input_file_lines() -> list[str]:
    input_file = INPUT_FOLDER / "input"
    input_text = input_file.read_text("UTF-8")
    return input_text.split("\n")
