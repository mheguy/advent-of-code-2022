from advent_of_code.dec_07.part_1 import (
    parse_text_input,
    Terminal,
    get_all_folders,
    Folder,
)
from shared_lib.utils import get_input_file_lines

FS_SPACE = 70000000
SPACE_NEEDED = 30000000


def get_space_needed(root: Folder) -> int:
    used_space = root.get_size()
    free_space = FS_SPACE - used_space
    return SPACE_NEEDED - free_space


def get_smallest_viable_folder(folders: list[Folder], minimum_size: int) -> Folder:
    viable_folders = (folder for folder in folders if folder.size >= minimum_size)
    return min(
        viable_folders,
        key=lambda x: x.get_size(),
    )


def main():
    text_lines = get_input_file_lines()
    command_blocks = parse_text_input(text_lines)
    terminal = Terminal()

    for command_block in command_blocks:
        terminal.process_command_block(command_block)

    folder = get_smallest_viable_folder(
        get_all_folders(terminal.root), get_space_needed(terminal.root)
    )
    print(f"{folder.name} - {folder.size}")


if __name__ == "__main__":
    main()
