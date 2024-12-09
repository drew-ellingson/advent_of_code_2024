from copy import copy
from typing import List


def p1(disk: List[str]) -> int:
    while True:
        if disk[-1] == ".":
            disk.pop()
            continue

        try:
            idx = disk.index(".")
        except ValueError:
            break

        disk[idx], disk[-1] = disk[-1], disk[idx]

    return sum(i * int(c) for i, c in enumerate(disk))


def p2(disk: List[str]) -> int:
    def move_file(p2_disk: List[str], i: int) -> None:
        idx = p2_disk.index(str(i))
        length = p2_disk.count(str(i))

        try:
            free_idx = min(
                i
                for i in range(len(p2_disk[:idx]))
                if all([a == "." for a in p2_disk[i : i + length]])
            )
        except ValueError:
            return None

        p2_disk[free_idx : free_idx + length], p2_disk[idx : idx + length] = (
            p2_disk[idx : idx + length],
            p2_disk[free_idx : free_idx + length],
        )

    def move_all_files(p2_disk: List[str]) -> None:
        max_idx = max(int(x) for x in p2_disk if x != ".")
        for i in range(max_idx, 0, -1):
            move_file(p2_disk, i)

    move_all_files(p2_disk)

    return sum(i * (0 if c == "." else int(c)) for i, c in enumerate(p2_disk))


with open("day_09/input.txt") as f:
    disk_map = f.read().strip()

disk = []
for i, c in enumerate(str(disk_map)):
    if i % 2 == 0:
        disk = disk + int(c) * [str(i // 2)]
    else:
        disk = disk + int(c) * ["."]

p2_disk = copy(disk)

print(f"P1 Soln is: {p1(disk)}")
print(f"P2 Soln is: {p2(p2_disk)}")
