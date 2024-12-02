from dataclasses import dataclass
from typing import List


@dataclass
class Report:
    levels: List[int]

    def is_safe(self, p2: bool = False) -> bool:
        def safe_subset(levels: List[int]) -> bool:
            # check monotonicity
            if levels != sorted(levels) and levels != list(reversed(sorted(levels))):
                return False

            # check diffs allowable
            diffs = [abs(levels[i] - levels[i - 1]) for i in range(1, len(levels))]
            return all(1 <= x <= 3 for x in diffs)

        if not p2:
            return safe_subset(self.levels)
        else:
            cands = [self.levels] + [
                self.levels[:i] + self.levels[i + 1 :] for i in range(len(self.levels))
            ]
            return any(safe_subset(c) for c in cands)


with open("day_02/input.txt") as f:
    reports = [Report([int(y) for y in x.strip().split(" ")]) for x in f.readlines()]

p1 = sum(1 for r in reports if r.is_safe())
p2 = sum(1 for r in reports if r.is_safe(p2=True))

print(f"P1 Solution is: {p1}")
print(f"P2 Solution is: {p2}")
