import re
from typing import Dict, Callable


def mult(instr: re.Match[str]) -> int:
    """mul(12,13) -> 156"""

    nums = list(map(int, instr.group()[4:-1].split(",")))
    return nums[0] * nums[1]


def mult_conditional(instr: re.Match[str], dos_n_donts: Dict[int, str]) -> int:
    # find 'do()' or 'don't()' most immdiately preceding instr
    max_lower_idx: Callable[[int], int] = lambda x: -1 if x > instr.start() else x
    status_idx = max(dos_n_donts, key=max_lower_idx)
    do = True if dos_n_donts[status_idx] == "do()" else False

    return mult(instr) if do else 0


with open("day_03/input.txt") as f:
    instructions = f.read()

mult_pattern = r"mul\(\d{1,3},\d{1,3}\)"
mult_matches = list(re.finditer(mult_pattern, instructions))

dos_n_donts_pattern = r"(do\(\)|don\'t\(\))"
dos_n_donts_matches = re.finditer(dos_n_donts_pattern, instructions)
dos_n_donts = {m.end(): m.group(0) for m in dos_n_donts_matches}
dos_n_donts[0] = "do()"  # start as 'on'

p1 = sum(mult(m) for m in mult_matches)
p2 = sum(mult_conditional(m, dos_n_donts) for m in mult_matches)

print(f"P1 Soln is: {p1}")
print(f"P2 Soln is: {p2}")
