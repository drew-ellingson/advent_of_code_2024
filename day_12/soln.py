from __future__ import annotations
from typing import List, Tuple


DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def _add(tup1: Tuple[int, int], tup2: Tuple[int, int]) -> Tuple[int, int]:
    """pointswise addition of same sized tuples"""
    return tuple(map(sum, zip(tup1, tup2)))


def get_connected_comps(coords: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
    """
    given a list of Tuples, return a list of connected components,
    where two points are connected if they differ by an element of DIRS

    eg. [(1,1), (1,2), (2,2), (3,3), (3,4), (4,5)] -> 
        [[(1,1), (1,2), (2,2)], [(3,3), (3,4)], [(4,5)]]
    """

    comps = []
    while coords:
        comp_complete = False
        comp = [coords[0]]
        while not comp_complete:
            neighbors = [_add(c, d) for c in comp for d in DIRS]

            adds = [n for n in neighbors if n in coords and n not in comp]
            if not adds:
                comp_complete = True

            comp = list(set(comp + adds))
            coords = [c for c in coords if c not in comp]
        comps.append(comp)
    return comps


def split_into_regions(grid: List[List[str]]) -> List[Region]:
    """Given input grid, create list of regions"""

    coords = [(i, j) for i in range(len(grid)) for j in range(len(grid[0]))]
    regions = []

    while coords:
        label = grid[coords[0][0]][coords[0][1]]
        same_label = [(i, j) for (i, j) in coords if grid[i][j] == label]
        label_regions = get_connected_comps(same_label)

        for lr in label_regions:
            regions.append(Region(label, lr))

        coords = [c for c in coords if c not in same_label]

    return regions


class Region:
    def __init__(self, label: str, coords: List[Tuple[int, int]]):
        self.label = label
        self.coords = coords

    def perimeter(self) -> int:
        """
        perimeter goes up by 1 if the neighbor of a point in the region is not contained
        in the region
        """
        perimeter = 0
        for c in self.coords:
            for d in DIRS:
                if _add(c, d) not in self.coords:
                    perimeter += 1
        return perimeter

    def area(self) -> int:
        return len(self.coords)

    def side_count(self) -> int:
        """
        eg. collect all points involved in a 'top' side, and then the connected
        component count of [points involved in a top side] gives you 'top side count'

        repeat for each type of side in [top, left, bottom, right]
        """

        top_points = [c for c in self.coords if _add(c, (-1, 0)) not in self.coords]
        bottom_points = [c for c in self.coords if _add(c, (1, 0)) not in self.coords]
        left_points = [c for c in self.coords if _add(c, (0, -1)) not in self.coords]
        right_points = [c for c in self.coords if _add(c, (0, 1)) not in self.coords]

        return sum(
            len(get_connected_comps(points))
            for points in [top_points, bottom_points, left_points, right_points]
        )

    def price(self, p2: bool = False) -> int:
        return (self.perimeter() if not p2 else self.side_count()) * self.area()


with open("day_12/input.txt") as f:
    grid = [[y for y in x.strip()] for x in f.readlines()]

regions = split_into_regions(grid)

print(f"P1 Soln is: {sum(r.price() for r in regions)}")
print(f"P2 Soln is: {sum(r.price(p2=True) for r in regions)}")
