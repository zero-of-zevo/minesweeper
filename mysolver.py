from game import *
import itertools
from typing import TypeAlias

offset: TypeAlias = tuple[int, int]



class Solve:
    def __init__(self, game:Game) -> None:
        self.game = game
        self.openedblocks:set[offset] = set() # (x, y)
        # self.mineblocks:dict[offset:float] = {} #(x, y): percentage
        for j in range(game.size[1]):
            for i in range(game.size[0]):
                if self.game.field[j][i].state == State.OPENED and not self.game.field[j][i].around == 0 :
                    self.openedblocks.add((i, j))
        self.validblocks:list[offset] = []
        self.minesets:list[
            tuple[
                list[offset], # centerblock. around
                list[offset], # aroundclosedblockes
                tuple[list[offset]] # combination of aroundclosedblockes
                ]
            ] = []

    def buildminesets(self):
        for x, y in self.openedblocks:
            aroundclosedblockes:list[offset] = []
            aroundflaggedblockes:list[offset] = []
            for j in (-1, 0, 1):
                for i in (-1, 0, 1):
                    if 0 <= y + j < self.game.size[1] and 0 <= x + i < self.game.size[0]:
                        if self.game.field[y + j][x + i].state == State.CLOSED:
                            aroundclosedblockes.add((x + i,y + j))
                        if self.game.field[y + j][x + i].state == State.FLAGGED:
                            aroundflaggedblockes.add((x + i,y + j))

            # if len(aroundclosedblockes) == self.game.field[y][x].around - len(aroundflaggedblockes):
            #    self.mineblocks.update(aroundclosedblockes)
            if self.game.field[y][x].around - len(aroundflaggedblockes) > 0:
                self.validblocks.add((x,y))
                self.minesets.add(
                    (
                        frozenset([(x,y)]),
                        frozenset(aroundclosedblockes),
                        tuple(set(list(map(
                            lambda x: frozenset(x), 
                            list(itertools.combinations(
                                list(aroundclosedblockes),
                                self.game.field[y][x].around - len(aroundflaggedblockes)
                                ))))
                         ))
                        )
                    )   
        self.solveminesets()

    
    def solveminesets(self):
        # self.clearvalid()
        minesetcouples = list(itertools.combinations(list(self.minesets), 2))
        newminesets:list[
            tuple[
                list[offset], # centerblock. around
                list[offset], # aroundclosedblockes
                tuple[list[offset]] # combination of aroundclosedblockes
                ]
            ] = []
        for d in minesetcouples:
            if len(list(d[0][1].intersection(d[1][1])))>0:
                newcenterblocks = d[0][0].union(d[1][0])
                newaround = d[0][1].union(d[1][1])

                intersctrions = d[0][1].intersection(d[1][1])
                newcombination:list[frozenset[offset]] = []
                for d0 in d[0][2]:
                    for d1 in d[1][2]:
                        if intersctrions.intersection(d0) == intersctrions.intersection(d0):
                            newcombination.append(d0.union(d1))
                newminesets.add((
                        newcenterblocks,
                        newaround,
                        tuple(newcombination)
                        ))
            else:
                newminesets.add(d[0])
                newminesets.add(d[1])
        print(list(minesetcouples)[2])
        print()
        print(list(self.minesets)[2])
        print()
        print(list(newminesets)[2])





























