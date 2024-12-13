from dataclasses import dataclass
from typing import List, Dict

import re
import sympy as sp


@dataclass
class Machine:
    buttonA: List[int]  # [x,y]
    buttonB: List[int]  # [x,y]
    prize: List[int]  # [x,y]

    def solve(
        self,
    ) -> Dict[
        sp.core.symbol.Symbol, sp.core.numbers.Rational | sp.core.numbers.Integer
    ]:

        a, b = sp.symbols("a b")

        eq1 = sp.Eq(self.buttonA[0] * a + self.buttonB[0] * b, self.prize[0])
        eq2 = sp.Eq(self.buttonA[1] * a + self.buttonB[1] * b, self.prize[1])

        return sp.solve((eq1, eq2), (a, b))

    def cost(self) -> int:
        x = self.solve()
        a, b = sp.symbols("a b")

        if all(isinstance(a, sp.core.numbers.Integer) for a in x.values()):
            return 3 * x[a] + x[b]
        else:
            return 0


def parse_machine(raw_machine, p2=False):
    b1, b2, prize = raw_machine.split("\n")
    x_reg, y_reg = r"X[\+|=](\d+),", r"Y[\+|=](\d+)"

    b1 = [int(re.search(x_reg, b1).group(1)), int(re.search(y_reg, b1).group(1))]
    b2 = [int(re.search(x_reg, b2).group(1)), int(re.search(y_reg, b2).group(1))]
    prize = [
        int(re.search(x_reg, prize).group(1)),
        int(re.search(y_reg, prize).group(1)),
    ]

    if p2:
        prize = [x + 10000000000000 for x in prize]

    return Machine(b1, b2, prize)


with open("day_13/input.txt") as f:
    raw_machines = f.read().split("\n\n")
    p1_machines = [parse_machine(m) for m in raw_machines]
    p2_machines = [parse_machine(m, p2=True) for m in raw_machines]

print(f"P1 Soln is: {sum(m.cost() for m in p1_machines)}")
print(f"P2 Soln is: {sum(m.cost() for m in p2_machines)}")
