from typing import Dict
from collections import defaultdict, Counter


def blink(stones: Dict[int, int]) -> Dict[int, int]:
    post_blink: Dict[int, int] = defaultdict(int)
    for s, mult in stones.items():
        if s == 0:
            post_blink[1] += mult
        elif len(str(s)) % 2 == 0:
            left, right = str(s)[: len(str(s)) // 2], str(s)[len(str(s)) // 2 :]
            post_blink[int(left)] += mult
            post_blink[int(right)] += mult
        else:
            post_blink[2024 * s] += mult
    return post_blink


def blink_many_times(stones: Dict[int, int], blink_count: int) -> Dict[int, int]:
    for _ in range(blink_count):
        stones = blink(stones)
    return stones


with open("day_11/input.txt") as f:
    stones = dict(Counter([int(x) for x in f.read().strip().split(" ")]))

print(f"P1 Soln is: {sum(blink_many_times(stones, 25).values())}")
print(f"P1 Soln is: {sum(blink_many_times(stones, 75).values())}")
