#MineSweeper Simulation
from random import sample
from dataclasses import dataclass
from enum import Enum
import numpy as np

class State(Enum):
    CLOSED = 0
    OPENED = 1
    FLAGGED = 2
    QUESTION = 3

@dataclass
class Cell:
    mine: bool = False
    count: int = 0
    
    state: State = State.CLOSED
    
    def __str__(self) -> str:
        if self.state == State.CLOSED:
            return '■'
        if self.state == State.FLAGGED:
            return '⚑'
        if self.state == State.QUESTION:
            return '?'
        if self.mine:
            return 'x'
        if self.count == 0:
            return ' '
        return str(self.count)

class Interaction(Enum):
    MINE = 0
    FLAG = 1
    QUESTION = 2

class Game:
    def __init__(self, x, y, mine, autorender=True) -> None:
        self.size = (x, y)
        self.minecount = mine
        self.board = [[Cell() for _ in range(x)] for _ in range(y)]
        self.mines = []
        self.is_over = False
        
        
        if autorender:
            BOARDPOS = [(i, j) for i in range(x) for j in range(y)]
            SPAWNSPOT:list[tuple[int, int]] = [(x//2+i-1, y//2+j-1) for i in range(-1, 2) for j in range(-1, 2)]
            while True:
                self.board = [[Cell() for _ in range(x)] for _ in range(y)]
                self.mines = sample(BOARDPOS, mine)
                self.render()
                if all(map(lambda x: not self.board[x[1]][x[0]].mine, SPAWNSPOT)):
                    break
                    
    def render(self):
        x, y = self.size
        for i, j in self.mines:
            self.board[j][i].mine = True
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= i + dx < x and 0 <= j + dy < y:
                        self.board[j + dy][i + dx].count += 1
    def sweep(self, x, y):
        self.board[y][x].state = State.OPENED
        if self.board[y][x].mine:
            self.is_over = True
            return True
        if self.board[y][x].count == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= x + dx < self.size[0] and 0 <= y + dy < self.size[1]:
                        if self.board[y + dy][x + dx].state == State.CLOSED:
                            self.sweep(x + dx, y + dy)
        self.is_over = False
        return False
    def flag(self, x, y):
        if self.board[y][x].state == State.CLOSED:
            self.board[y][x].state = State.FLAGGED
    def question(self, x, y):
        if self.board[y][x].state == State.CLOSED:
            self.board[y][x].state = State.QUESTION
    def do(self, interaction: Interaction, x, y):
        if interaction == Interaction.MINE:
            self.sweep(x, y)
        if interaction == Interaction.FLAG:
            self.flag(x, y)
        if interaction == Interaction.QUESTION:
            self.question(x, y)
    @property
    def numericboard(self) -> np.ndarray:
        return np.array([[cell.count if cell.state == State.OPENED else
                        9 if cell.state == State.CLOSED else
                        10 if cell.state == State.FLAGGED else 11 for cell in row] for row in self.board])
    @property
    def is_win(self):
        return all((cell.mine and cell.state == State.FLAGGED) or cell.state == State.OPENED for row in self.board for cell in row)
    @property
    def leftmine(self):
        return self.minecount - sum(cell.state == State.FLAGGED for row in self.board for cell in row)
    def __str__(self) -> str:
        return '\n'.join([' '.join(map(str, row)) for row in self.board])


# g = Game(10, 10, 10)
# while True:
#     print(g)
#     print(g.sweep(*map(int, input().split())))