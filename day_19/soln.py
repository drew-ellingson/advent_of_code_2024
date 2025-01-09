from dataclasses import dataclass
from typing import List 


@dataclass
class TowelSet:
    available: List[str]
    patterns: List[str]

    def is_possible(self, pattern):
        if pattern in self.available:
            return True 
        else:
            cands = [pattern.replace(a, '', 1) for a in self.available if pattern.startswith(a)]
            return any(self.is_possible(c) for c in cands)

    def possible_count(self):
        # count = 0
        # for i, p in enumerate(self.patterns):
        #     if self.is_possible(p):
        #         count += 1
        #     print(f'done {i} / {len(self.patterns)} for {100*round(i / len(self.patterns), 4)}')
        # return count 
    
        return len([p for p in self.patterns if self.is_possible(p)])


with open('day_19/input_sample.txt') as f:
    available, patterns = f.read().split('\n\n')

    available = available.strip().split(', ')
    patterns = patterns.split('\n')

ts = TowelSet(available, patterns)

print(ts)
print(ts.possible_count())