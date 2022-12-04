from typing import Iterable

from shared_lib.resources import INPUT_FOLDER


def get_input_file_lines() -> Iterable[str]:
    input_file = INPUT_FOLDER / "input"
    input_text = input_file.read_text("UTF-8")
    lines = input_text.split("\n")
    for line in lines:
        if line:
            yield line
        else:
            return
