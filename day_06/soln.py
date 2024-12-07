from dataclasses import dataclass, field
from typing import List, Tuple, Callable, Optional
from copy import deepcopy


def add(tup1: Tuple[int, ...], tup2: Tuple[int, ...]) -> Tuple[int, ...]:
    # keeping mypy at needlessly high strictness so i get to do fun stuff like this
    mysum: Callable[[Tuple[int, ...]], int] = sum
    return tuple(map(mysum, zip(tup1, tup2)))


def mult(scal: int, tup: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(scal * a for a in tup)


@dataclass
class Point:
    val: str
    visited: bool = False

    # keep track of what directions a point has been visited from to detect loops
    visit_dirs: List[Optional[Tuple[int, int]]] = field(default_factory=lambda: [])


@dataclass
class GridTrav:
    grid: List[List[Point]]
    vec: Tuple[int, int] = (-1, 0)  # up
    loop: bool = False

    guard_pos: Tuple[int, int] = field(init=False)
    w: int = field(init=False)
    h: int = field(init=False)

    def __post_init__(self) -> None:
        self.h = len(self.grid)
        self.w = len(self.grid[0])

        for i, row in enumerate(self.grid):
            if "^" in [x.val for x in row]:
                j = [x.val for x in row].index("^")
                self.guard_pos = (i, j)
                self.grid[i][j].val = "."
                self.grid[i][j].visited = True

    def one_step(self) -> None:
        next_step_valid = False
        next_vec = {(-1, 0): (0, 1), (0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0)}

        while not next_step_valid:
            i, j = add(self.guard_pos, self.vec)
            if i < 0 or i >= self.h or j < 0 or j >= self.w:
                raise IndexError("This step takes you out of bounds")
            elif self.grid[i][j].val == "#":
                self.vec = next_vec[self.vec]
            else:
                next_step_valid = True
                self.guard_pos = (i, j)

                if self.grid[i][j].visited and self.vec in self.grid[i][j].visit_dirs:
                    self.loop = True

                self.grid[i][j].visited = True
                self.grid[i][j].visit_dirs.append(self.vec)

    def count_step(self) -> int:
        try:
            while True:
                self.one_step()
        except IndexError:
            return len([x for row in self.grid for x in row if x.visited])

    def obstruction_makes_loop(self, i: int, j: int) -> bool:
        if self.grid[i][j].val == "#":
            return False

        if (i, j) == self.guard_pos:
            return False

        self.grid[i][j].val = "#"

        try:
            while not self.loop:
                self.one_step()
        except IndexError:
            return False

        return True


with open("day_06/input.txt") as f:
    grid = GridTrav([[Point(x) for x in row.strip()] for row in f.readlines()])

p1 = deepcopy(grid).count_step()

print(f"P1 Soln is: {p1}")

count = 0
for i in range(grid.h):
    for j in range(grid.w):
        grid_ij = deepcopy(grid)
        if grid_ij.obstruction_makes_loop(i, j):
            count += 1

print(f"P2 Soln is: {count}")
