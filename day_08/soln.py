from typing import List, Tuple, Dict
from dataclasses import dataclass, field
from itertools import combinations, chain


@dataclass
class Grid:
    grid: List[List[str]]
    w: int = field(init=False)
    h: int = field(init=False)

    def __post_init__(self) -> None:
        self.h = len(self.grid)
        self.w = len(self.grid[0])

    def get_distinct_node_labels(self) -> List[str]:
        return list(set([val for row in self.grid for val in row if val != "."]))

    def get_node_locs(self, label: str) -> List[Tuple[int, int]]:
        return [
            (i, j)
            for i in range(self.h)
            for j in range(self.w)
            if self.grid[i][j] == label
        ]

    def antinode_locs(self, label: str, p2: bool = False) -> List[Tuple[int, int]]:
        """given a list of node coords of same type, find antinode coords"""
        nodes = self.get_node_locs(label)
        pairs = combinations(nodes, 2)

        antinodes = []
        for p, q in pairs:
            x_d, y_d = q[0] - p[0], q[1] - p[1]

            if not p2:
                new1, new2 = (p[0] - x_d, p[1] - y_d), (q[0] + x_d, q[1] + y_d)
                antinodes.extend([new1, new2])
            else:
                # some safe upper bound to ensure antinodes propogate past end of grid
                safe_range = self.h // min(abs(x_d), abs(y_d))
                news1 = [(p[0] - i * x_d, p[1] - i * y_d) for i in range(safe_range)]
                news2 = [(q[0] + i * x_d, q[1] + i * y_d) for i in range(safe_range)]
                antinodes.extend(news1)
                antinodes.extend(news2)

        antinodes = [
            (x, y) for x, y in antinodes if 0 <= x < self.h and 0 <= y < self.w
        ]

        return antinodes

    def get_all_antinode_locs(
        self, p2: bool = False
    ) -> Dict[str, List[Tuple[int, int]]]:
        labels = self.get_distinct_node_labels()
        antinodes = {}

        for label in labels:
            antinodes[label] = [(x, y) for x, y in self.antinode_locs(label, p2=p2)]

        return antinodes

    def count_distinct_antinode_locs(self, p2: bool = False) -> int:
        antinodes = self.get_all_antinode_locs(p2=p2)

        locs = chain(*[v for v in antinodes.values()])

        return len(set(list(locs)))


with open("day_08/input.txt") as f:
    pts = [[y for y in row.strip()] for row in f.readlines()]

g = Grid(pts)

print(f"P1 Soln is: {g.count_distinct_antinode_locs()}")
print(f"P2 Soln is: {g.count_distinct_antinode_locs(p2=True)}")
