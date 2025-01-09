from typing import Tuple
from functools import lru_cache


@lru_cache
def count_ways_one(available: Tuple[str], pattern: str) -> bool:
    if not pattern:
        return 1
    else:
        cands = [pattern.replace(a, "", 1) for a in available if pattern.startswith(a)]
        return sum(count_ways_one(available, c) for c in cands)


def count_ways_all(available: Tuple[str], patterns: Tuple[str], p2: bool = False) -> int:
    counts = [count_ways_one(available, p) for p in patterns]
    return len([c for c in counts if c > 0]) if not p2 else sum(counts)


with open("day_19/input.txt") as f:
    available, patterns = f.read().split("\n\n")
    available = tuple(available.strip().split(", "))
    patterns = tuple(patterns.split("\n"))

print(f"P1 Soln is: {count_ways_all(available, patterns)}")
print(f"P2 Soln is: {count_ways_all(available, patterns, p2=True)}")
