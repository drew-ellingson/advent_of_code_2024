from typing import List


class Pages:
    def __init__(self, pages: List[int]):
        self.pages = pages

    def observes_rule(self, first: int, second: int) -> bool:
        if first not in self.pages or second not in self.pages:
            return True
        if self.pages.index(first) < self.pages.index(second):
            return True
        return False

    def order_correctly(self, ruleset: List[List[int]]) -> List[int]:
        while not all(self.observes_rule(*r) for r in ruleset):
            for r in ruleset:
                if not self.observes_rule(*r):
                    first_idx, second_idx = self.pages.index(r[0]), self.pages.index(
                        r[1]
                    )
                    self.pages[first_idx], self.pages[second_idx] = (
                        self.pages[second_idx],
                        self.pages[first_idx],
                    )
        return self.pages


with open("day_05/input.txt") as f:
    rules_raw, pages_raw = f.read().split("\n\n")
    rules = [[int(y) for y in x.strip().split("|")] for x in rules_raw.split("\n")]
    pages = [
        Pages([int(y) for y in x.strip().split(",")]) for x in pages_raw.split("\n")
    ]

p1 = sum(
    p.pages[len(p.pages) // 2] for p in pages if all(p.observes_rule(*r) for r in rules)
)

incorrects = [p for p in pages if not all(p.observes_rule(*r) for r in rules)]
p2 = sum(p.order_correctly(rules)[len(p.pages) // 2] for p in incorrects)

print(f"P1 Soln is: {p1}")
print(f"P2 Soln is: {p2}")
