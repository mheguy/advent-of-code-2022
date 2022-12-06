from pathlib import Path

root_folder = Path(__file__).parent

for i in range(5, 25):
    i += 1
    day_folder = root_folder / f"dec_{i:02d}"
    day_folder.mkdir(exist_ok=True)

    for part in range(2):
        part_file = day_folder / f"part_{part + 1}.py"
        part_file.write_text(
            """def main():
    ...


if __name__ == "__main__":
    main()
"""
        )
        # part_file.touch(exist_ok=True)
