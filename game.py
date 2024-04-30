import random
from enum import Enum
from dataclasses import dataclass
from random import sample
from typing import Any, Literal, NoReturn, cast, overload
import numpy as np
NDArray = np.ndarray

class State(Enum):
    CLOSED = 0
    OPENED = 1
    FLAGGED = 2

@dataclass
class Block:
    ismine: bool = False
    around: int = 0
    state: State = State.CLOSED
    
    def __str__(self) -> str:
        if self.state == State.CLOSED:
            return '■'
        if self.state == State.FLAGGED:
            return '⚑'
        if self.ismine:
            return 'ㅗ'
        if self.around == 0:
            return ' '
        else: return str(self.around)
    
class Interaction(Enum):
    OPEN = 0
    FLAG = 1

class Game():
    def __init__(self, x, y, count_of_mines):
        self.size = (x,y)
        self.minecount = count_of_mines
        self.field = [[Block() for _ in range(x)] for _ in range(y)]
        self.gameover = False
        self.isbuilt = False

    def build(self, fx, fy):
        x, y = self.size
        self.mines = sample([(i, j) for i in range(x) for j in range(y) if (i, j) not in [(fx + fax, fy+ fay) for fax in [-2,-1, 0, 1, 2] for fay in [-2,-1, 0, 1, 2]]] , self.minecount)
        for i, j in self.mines:
            self.field[j][i].ismine = True
            for pi in [-1, 0, 1]:
                for pj in [-1, 0, 1]:
                    if 0 <= i + pi < x and 0 <= j + pj < y:
                        self.field[j+pj][i+pi].around +=1
        self.isbuilt = True
    
    def open(self, i, j):
        self.field[j][i].state = State.OPENED
        x, y = self.size
        if not self.isbuilt:
            self.build(i, j)
        if self.field[j][i].ismine:
            self.gameover = True
            return True
        if self.field[j][i].around == 0:
            for pi in [-1, 0, 1]:
                for pj in [-1, 0, 1]:
                    if 0 <= i + pi < x and 0 <= j + pj < y:
                        if self.field[j + pj][i + pi].state == State.CLOSED:
                            self.open(i+pi, j+pj)
        self.gameover = False
        return False
    def flag(self, x, y):
        if self.field[y][x].state == State.CLOSED:
            self.field[y][x].state = State.FLAGGED
    def interact(self, interaction: Interaction, x, y):
        if interaction == Interaction.OPEN:
            self.open(x, y)
        if interaction == Interaction.FLAG:
            self.flag(x, y)

    @property
    def is_win(self):
        return all((i.ismine and i.state == State.FLAGGED) or i.state == State.OPENED for j in self.field for i in j)
    
    @property
    def leftmine(self):
        return self.minecount - sum(i.state == State.FLAGGED for j in self.field for i in j)
    @overload
    def getintegerfield(self, isstr: Literal[True], isnp: Literal[False]) -> list[list[str]]: pass
    @overload
    def getintegerfield(self, isstr: Literal[False], isnp: Literal[False]) -> list[list[int]]: pass
    @overload
    def getintegerfield(self, isstr: Literal[True], isnp: Literal[True]) -> NoReturn: pass
    @overload
    def getintegerfield(self, isstr: Literal[False], isnp: Literal[True]) -> NDArray: pass
    def getintegerfield(self, isstr = False, isnp = False):
        fill = 9 if isstr else " "
        data: list[list[str | int]] = [[fill for _ in range(self.size[0])] for _ in range(self.size[1])]
        if isstr:
            for j in range(self.size[0]):
                for i in range(self.size[1]):
                    if self.field[j][i].state == State.OPENED:
                        data[j][i] = str(self.field[j][i].around)
                    elif self.field[j][i].state == State.FLAGGED:
                        data[j][i] = str(10)
                    else:
                        data[j][i] = str(9)
            return cast(list[list[str]], data)
        else:
            for j in range(self.size[0]):
                for i in range(self.size[1]):
                    if self.field[j][i].state == State.OPENED:
                        data[j][i] = self.field[j][i].around
                    elif self.field[j][i].state == State.FLAGGED:
                        data[j][i] = 10
                    else:
                        data[j][i] = 9
            if isnp:
                return np.array(cast(list[list[int]], data))
            return cast(list[list[int]], data)

    def __str__(self):
        return '\n'.join([' '.join(map(str, j)) for j in self.field])