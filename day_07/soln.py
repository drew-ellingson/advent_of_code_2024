from typing import List, Tuple, Dict, Callable
from dataclasses import dataclass
from itertools import product

P1_OPS = ["+", "*"]
P2_OPS = ["+", "*", "||"]

OPS_MEMO = {}


def parse_eq(raw_eq: str) -> Tuple[int, List[int]]:
    raw_target, raw_operands = raw_eq.split(": ")
    target = int(raw_target)
    operands = [int(x) for x in raw_operands.split(" ")]
    return target, operands


@dataclass
class UnfinishedEq:
    target: int
    operands: List[int]

    def any_valid_eqs(self, part: str = "p1") -> bool:
        valid_ops = P1_OPS if part == "p1" else P2_OPS
        lookup_key = "|".join([part, str(len(self.operands))])

        # memoize the itertools step to speed up a bit maybe
        if lookup_key not in OPS_MEMO:
            OPS_MEMO[lookup_key] = list(
                product(valid_ops, repeat=len(self.operands) - 1)
            )

        eq_ops = OPS_MEMO[lookup_key]

        for eo in eq_ops:
            output = self.operands[0]
            for i, o in enumerate(eo):
                get_op: Dict[str, Callable[[int], int]] = {
                    "+": output.__add__,
                    "*": output.__mul__,
                    "||": lambda x: int("".join([str(output), str(x)])),
                }
                output = get_op[o](self.operands[i + 1])

                # all ops non-decreasing
                if output > self.target:
                    break

            if output == self.target:
                return True
        return False


with open("day_07/input.txt") as f:
    eqs = [UnfinishedEq(*parse_eq(line)) for line in f.readlines()]

p1 = sum(eq.target for eq in eqs if eq.any_valid_eqs(part="p1"))
p2 = sum(eq.target for eq in eqs if eq.any_valid_eqs(part="p2"))

print(f"P1 Soln is: {p1}")
print(f"P2 Soln is: {p2}")
