from dataclasses import dataclass, field
from typing import Tuple, Optional, List

DIRS = {'^': (-1, 0), 
        'v': (1,0), 
        '>': (0,1), 
        '<': (0,-1)
}

TURN_POINTS = {
    ('>','>'): 0,
    ('>','^'): 1000,
    ('>','<'): 2000,
    ('>','v'): 1000,
    ('^','>'): 1000,
    ('^','^'): 0,
    ('^','<'): 1000,
    ('^','v'): 2000,
    ('<','>'): 2000,
    ('<','^'): 1000,
    ('<','<'): 0,
    ('<','v'): 1000,
    ('v','>'): 1000,
    ('v','^'): 2000,
    ('v','<'): 1000,
    ('v','v'): 0,

}

def _add(tup1, tup2):
    return tuple(map(sum, zip(tup1, tup2)))

@dataclass 
class NodeTraversal:
    coord: Tuple[int, int]
    visited: bool = False
    
    path: List[Tuple[int, int]] = field(default_factory = lambda: [])

    distance: int = 1e100 
    visit_direction: Optional[str] = None 

@dataclass 
class Traversal(list):
    nodes: List[NodeTraversal]
    idx = 0

    def __iter__(self):
        return self 
    
    def __next__(self):
        if self.idx < len(self.nodes):
            value = self.nodes[self.idx]
            self.idx += 1
            return value 
        else:
            raise StopIteration 

    def get_by_coord(self, coord):
        return [x for x in self.nodes if x.coord == coord][0]

class Grid:
    def __init__(self, grid):
        self.grid = grid 

        self.h = len(self.grid)
        self.w = len(self.grid[0])
        self.start = [(i,j) for i in range(self.h) for j in range(self.w) if self.grid[i][j] == 'S'][0]
        self.end = [(i,j) for i in range(self.h) for j in range(self.w) if self.grid[i][j] == 'E'][0]

    def __repr__(self):
        msg = '' 
        for row in self.grid:
            msg = msg + ''.join(row) + '\n'
        return msg 

    def get_neighbors(self, coord):
        cands = {d: _add(coord, v) for d, v in DIRS.items()}
        return {d: (i,j) for d,(i,j) in cands.items() if 0 <= i < self.h and 0 <= j < self.w and self.grid[i][j] != '#'}

    def solve(self):
        t = Traversal([NodeTraversal((i,j)) for i in range(self.h) for j in range(self.w)])
        t.get_by_coord(self.start).visit_direction = '>'
        t.get_by_coord(self.start).distance = 0
        t.get_by_coord(self.start).path = [self.start]

        while not t.get_by_coord(self.end).visited:
            curr_node = min(t.nodes, key = lambda x: x.distance if not x.visited else 1e200)
            for d,n in self.get_neighbors(curr_node.coord).items():
                n_dist = curr_node.distance + 1 + TURN_POINTS[(curr_node.visit_direction, d)]
                if n_dist <= t.get_by_coord(n).distance:
                    t.get_by_coord(n).visit_direction = d
                    
                    if n_dist == t.get_by_coord(n).distance:
                        t.get_by_coord(n).path = list(set(curr_node.path + t.get_by_coord(n).path))
                    else:
                        t.get_by_coord(n).path = curr_node.path + [n]
                    
                    t.get_by_coord(n).distance = n_dist
        
            curr_node.visited = True
        
        msg = ''
        path = t.get_by_coord(self.end).path 
        for i in range(self.h):
            msg = msg + ''.join('O' if (i,j) in path else self.grid[i][j] for j in range(self.w)) + '\n'
        print(msg)
                            
        return t.get_by_coord(self.end).distance, len(t.get_by_coord(self.end).path)

with open('day_16/input_sample2.txt') as f:
    g = Grid([[y for y in x.strip()] for x in f.readlines()])

print(f'P1 Soln is: {g.solve()}')
