from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from collections import defaultdict, Counter
import math


def _add(tup1: Tuple[int, int], tup2: Tuple[int, int], bound: Tuple[int, int]):
    """adds two tuples pointwise, but wraps around a given tuple of boundaries"""

    new = tuple(map(sum, zip(tup1, tup2)))
    return tuple(new[i] % bound[i] for i in range(len(new)))


def parse(raw_robot: str) -> Robot:
    p, v = raw_robot.split(" ")
    p = tuple(int(x) for x in p.replace("p=", "").split(","))
    v = tuple(int(x) for x in v.replace("v=", "").split(","))
    return Robot(p, v)


@dataclass
class Robot:
    pos: Tuple[int, int]
    vel: Tuple[int, int]


class Grid:
    def __init__(self, h: int, w: int, robots: List[Robot]):
        self.w = w
        self.h = h
        self.robots = robots

    def __repr__(self) -> str:
        msg = ""
        for i in range(self.h):
            row = "".join(
                str(sum(1 if r.pos == (j, i) else 0 for r in self.robots))
                for j in range(self.w)
            )
            msg = msg + row.replace("0", ".") + "\n"
        return msg

    def move_robots(self, seconds: int = 1) -> None:
        for _ in range(seconds):
            for r in robots:
                r.pos = _add(r.pos, r.vel, (w, h))

    def safety_score(self) -> int:
        w_mid, h_mid = w // 2, h // 2

        quad_scores = defaultdict(int)

        for r in self.robots:
            if w_mid + 1 <= r.pos[0] < self.w and r.pos[1] < h_mid:
                quad_scores[0] += 1
            elif r.pos[0] < w_mid and r.pos[1] < h_mid:
                quad_scores[1] += 1
            elif r.pos[0] < w_mid and h_mid + 1 <= r.pos[1] < self.h:
                quad_scores[2] += 1
            elif w_mid + 1 <= r.pos[0] < self.w and h_mid + 1 <= r.pos[1] < self.h:
                quad_scores[3] += 1

        return math.prod(quad_scores.values())

    def max_robots_in_row(self) -> int:
        return max(Counter(r.pos[1] for r in self.robots).values())

    def max_robots_in_col(self) -> int:
        return max(Counter(r.pos[0] for r in self.robots).values())


with open("day_14/input.txt") as f:
    robots = [parse(r.strip()) for r in f.readlines()]

h, w = 103, 101
grid = Grid(h, w, robots)

grid.move_robots(seconds=100)
print(f"P1 Soln is: {grid.safety_score()}")


i = 100
done = False
while not done:
    grid.move_robots()
    i += 1
    if grid.max_robots_in_col() >= 20 and grid.max_robots_in_row() >= 20:

        print(str(grid))
        print(f"P2 Soln is, as long as the above is a christmas tree, {i}")
        done = True
