from collections import deque
from pathlib import Path

CYPHER_LENGTH = 4
input_text = (Path(__file__).parent.parent.parent / "input/input").read_text("UTF-8")
cypher = deque([], CYPHER_LENGTH)
for pos, char in enumerate(input_text, start=1):
    cypher.append(char)
    if len(cypher) == CYPHER_LENGTH and len(set(cypher)) == CYPHER_LENGTH:
        print(pos)
        break
