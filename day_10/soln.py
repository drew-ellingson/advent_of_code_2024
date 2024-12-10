from typing import List, Tuple


class TopoMap:
    def __init__(self, grid: List[List[int]]) -> None:
        self.grid = grid
        self.h = len(self.grid)
        self.w = len(self.grid[0])

    def __repr__(self) -> str:
        msg = ""
        for row in grid:
            msg = msg + "".join(str(x) for x in row) + "\n"
        return msg

    def trail_next_step(
        self, trail: List[Tuple[int, int]]
    ) -> List[List[Tuple[int, int]]]:
        """takes a trail, returns a list of trails with the next possible steps taken"""

        trails = []
        x, y = trail[-1]
        h = self.grid[x][y]
        cands = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

        for c1, c2 in cands:
            if 0 <= c1 < self.h and 0 <= c2 < self.w:
                if self.grid[c1][c2] == h + 1:
                    trails.append(trail + [(c1, c2)])

        return trails

    def get_trailhead_score(self, trailhead: Tuple[int, int], p2: bool = False) -> int:
        trails = [[trailhead]]

        while self.grid[trails[0][-1][0]][trails[0][-1][1]] != 9:
            next_iter_trails = []
            for t in trails:
                next_iter_trails.extend(self.trail_next_step(t))
            if not next_iter_trails:
                return 0
            trails = next_iter_trails

        trail_ends = [t[-1] for t in trails]

        return len(set((tuple(t) for t in trails) if p2 else trail_ends))

    def get_total_score(self, p2: bool = False) -> int:
        trailheads = [
            (i, j)
            for i in range(len(self.grid))
            for j in range(len(self.grid[0]))
            if self.grid[i][j] == 0
        ]
        total_score = sum(self.get_trailhead_score(th, p2=p2) for th in trailheads)
        return total_score


with open("day_10/input.txt") as f:
    grid = [[int(x) for x in row.strip()] for row in f.readlines()]

tm = TopoMap(grid)

print(f"P1 Soln is: {tm.get_total_score()}")
print(f"P2 Soln is: {tm.get_total_score(p2=True)}")
