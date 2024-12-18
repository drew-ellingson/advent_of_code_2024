
MOVES = {
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
    '^': (-1, 0)
}

def _add(tup1, tup2):
    return tuple(map(sum, zip(tup1, tup2)))

class Warehouse:
    def __init__(self, grid):
        self.grid = grid 

    def __repr__(self):
        msg = ''
        for row in self.grid:
            msg = msg + ''.join(y for y in row) + '\n' 
        return msg 

    def c_get(self, coord):
        return self.grid[coord[0]][coord[1]]

    def c_set(self, coord, val):
        self.grid[coord[0]][coord[1]] = val

    def robot_pos(self):
        return [(i,j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == '@'][0]    
    
    def move(self, move_dir, coords):
        last_pos = coords[-1]

        cand = _add(last_pos, move_dir)

        if self.c_get(cand) == '.':
            for c in reversed(coords):
                self.c_set(_add(c, move_dir), self.c_get(c))
            self.c_set(coords[0], '.')
        elif self.c_get(cand) == 'O':
            coords.append(cand)
            self.move(move_dir, coords) 
        elif self.c_get(cand) == '#':
            return None
        else:
            raise ValueError(f'got an unexpected value {self.get.grid(cand)}')


    def execute_move_list(self, movelist):
        for m in movelist:
            self.move(MOVES[m], [self.robot_pos()])

    def gps_score(self):
        boxes = [(i,j) for i in range(len(self.grid)) for j in range(len(self.grid[0])) if self.grid[i][j] == 'O']
        return sum(100 * i + j for (i,j) in boxes)

with open('day_15/input.txt') as f:
    grid, movelist = f.read().split('\n\n')
    grid = [[y for y in row] for row in grid.split('\n')]
    movelist = list(movelist.replace('\n', ''))

wh = Warehouse(grid)
wh.execute_move_list(movelist)

print(wh.gps_score())