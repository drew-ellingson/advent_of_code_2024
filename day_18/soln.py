from collections import defaultdict
from typing import Tuple, List, Set, Dict

DIRS = [(1, 0), (-1, 0), (0, -1), (0, 1)]


def _add(tup1: Tuple[int, ...], tup2: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(map(sum, zip(tup1, tup2)))


class GridGraph:
    def __init__(self, h: int, w: int, obstructions: List[Tuple[int, int]]) -> None:
        self.h = h
        self.w = w
        self.obstructions = obstructions

        self.graph: Dict[Tuple[int, int], Set[Tuple[int, int]]] = defaultdict(set)
        self.gen_edges()

    def gen_edges(self) -> None:
        for i in range(self.w):
            for j in range(self.h):
                for d in DIRS:
                    cand = _add((i, j), d)
                    if 0 <= cand[0] < self.w and 0 <= cand[1] < self.h:
                        self.graph[(i, j)].add(cand)

    def min_path(
        self, start: Tuple[int, int], end: Tuple[int, int], obs_count: int = 1024
    ):
        unvisited = {n: 10000 for n in self.graph}
        unvisited[start] = 0

        while unvisited[end] == 10000 and any(x < 10000 for x in unvisited.values()):
            curr_node = min(unvisited, key=lambda x: unvisited[x])
            nbrs = [
                n
                for n in self.graph[curr_node]
                if n not in self.obstructions[:obs_count] and n in unvisited
            ]

            for n in nbrs:
                unvisited[n] = min(unvisited[n], unvisited[curr_node] + 1)

            unvisited.pop(curr_node)

        return unvisited[end]

    def first_blocking_obs(self) -> Tuple[int, int]:
        """faster to do some binary search something but im tired and gonna go to bed"""
        blocked = False
        i = 0

        while not blocked:
            i += 1

            if self.min_path((0, 0), (self.w - 1, self.h - 1), i) == 10000:
                blocked = True

        return self.obstructions[i - 1]


with open("day_18/input.txt") as f:
    pairs = [tuple(map(int, x.strip().split(","))) for x in f.readlines()]

H, W = 71, 71

gg = GridGraph(H, W, pairs)

print(f"P1 Soln is: {gg.min_path((0, 0), (W - 1, H - 1))}")
print(f"P2 Soln is: {gg.first_blocking_obs()}")
