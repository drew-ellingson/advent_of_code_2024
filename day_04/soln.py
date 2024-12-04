from typing import List, Tuple, Callable


def add(tup1: Tuple[int, ...], tup2: Tuple[int, ...]) -> Tuple[int, ...]:
    # still keeping mypy at needless high strictness so i get to do fun stuff like this
    mysum: Callable[[Tuple[int, ...]], int] = sum
    return tuple(map(mysum, zip(tup1, tup2)))


def mult(scal: int, tup: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(scal * a for a in tup)


class WordSearch:
    def __init__(self, grid: List[List[str]]):
        self.grid = grid
        self.h = len(self.grid)
        self.w = len(self.grid[0])

    def word_count(self, word: str) -> int:
        dirs = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
        word_len = len(word)
        count = 0

        for i in range(self.h):
            for j in range(self.w):
                for d in dirs:
                    cand = ""
                    for k in range(word_len):
                        coord = add((i, j), mult(k, d))

                        # assuming input is always sq here
                        if any(x < 0 or x >= self.w for x in coord):
                            break

                        cand = cand + self.grid[coord[0]][coord[1]]

                    if cand == word:
                        count += 1
        return count

    def x_mas_count(self) -> int:
        count = 0
        for i in range(1, self.h - 1):
            for j in range(1, self.w - 1):
                if self.grid[i][j] != "A":
                    continue
                if set((self.grid[i - 1][j - 1], self.grid[i + 1][j + 1])) != set(
                    ("M", "S")
                ):
                    continue
                if set((self.grid[i - 1][j + 1], self.grid[i + 1][j - 1])) != set(
                    ("M", "S")
                ):
                    continue
                count += 1
        return count


with open("day_04/input.txt") as f:
    grid = [[y for y in x.strip()] for x in f.readlines()]

ws = WordSearch(grid)

print(ws.word_count("XMAS"))

print(ws.x_mas_count())
