from collections import deque

from shared_lib.utils import get_input_file_text


def main(cypher_length):
    input_text = get_input_file_text()
    cypher = deque([], cypher_length)

    for pos, char in enumerate(input_text, start=1):
        cypher.append(char)
        if len(cypher) == cypher_length and len(set(cypher)) == cypher_length:
            print(pos)
            break


if __name__ == "__main__":
    main(4)
